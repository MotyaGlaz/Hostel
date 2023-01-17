import pandas as pd


def get_type_room(conn):
    return pd.read_sql('''
        SELECT
            type_id,
            type_name,
            (COUNT(room_id)) AS count_type
        FROM room
            INNER JOIN room_type USING (type_id)
        GROUP BY type_id
        -- ORDER BY type_name
    ''', conn)


def get_description_room(conn):
    return pd.read_sql('''
        SELECT
            description_id,
            description,
            detailed_description,
            (COUNT(room_id)) AS count_type
        FROM room
            INNER JOIN room_description USING (description_id)
        GROUP BY description_id
    ''', conn)


def get_service(conn):
    return pd.read_sql('''
        SELECT
            service_id,
            service_name,
            price
        FROM service
        GROUP BY service_id
    ''', conn)


def get_client(conn):
    return pd.read_sql('''
        SELECT 
            client_id,
            client_name,
            passport,
            phone
        FROM client
    ''', conn)


# Получение свободных номеров по типу и описанию
def get_available_type(conn, check_in, check_out, rooms_type, rooms_description):
    return pd.read_sql(f'''
        SELECT 
            description, 
            type_name, 
            price,
            price * CAST((JULIANDAY(:c_out) - JULIANDAY(:c_in) + 1) AS INTEGER) AS full_price, 
            detailed_description, 
            type_id, 
            description_id
        FROM room
            INNER JOIN room_type USING (type_id)
            INNER JOIN room_description USING (description_id)
        WHERE room_id NOT IN (SELECT room_id
                                FROM booking
                                WHERE status_id = 1 AND
                                    ((date_check_out >= :c_in AND date_check_in <= :c_in) OR 
                                    (date_check_in <= :c_out AND date_check_out >= :c_out) OR
                                    (date_check_in >= :c_in AND date_check_out <= :c_out)))       
            AND room_id IN (SELECT room_id
                            FROM room INNER JOIN room_type USING (type_id)
                            WHERE type_id IN ({str(rooms_type).strip('[]')})) 
            AND room_id IN (SELECT room_id
                            FROM room INNER JOIN room_description USING (description_id)
                            WHERE description_id IN ({str(rooms_description).strip('[]')})) 
        GROUP BY type_id, description_id
   ''', conn, params={"c_in": check_in, "c_out": check_out})


# Создание бронирования на основе предпочтений данных пользователя
def make_booking(conn, check_in, check_out, type_id, description_id, client_id, service_list):
    # получение самого первого подходящего номера
    get_room_id = int(pd.read_sql('''
        SELECT MIN(room_id) AS number_room
        FROM room
            INNER JOIN room_type USING (type_id)
            INNER JOIN room_description USING (description_id)
        WHERE room_id NOT IN (SELECT room_id
                                FROM booking
                                WHERE status_id = 1 AND
                                    ((date_check_out >= :c_in AND date_check_in <= :c_in) OR 
                                    (date_check_in <= :c_out AND date_check_out >= :c_out) OR
                                    (date_check_in >= :c_in AND date_check_out <= :c_out)))       
            AND type_id = :t_id AND description_id = :d_id
    ''', conn, params={"c_in": check_in, "c_out": check_out,
                       "t_id": type_id, "d_id": description_id})['number_room'].iloc[0])

    # бронирование по первому номеру
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO booking(room_id, client_id, status_id, date_check_in, date_check_out) 
        VALUES
            (:r_id, :c_id, 1, :c_in, :c_out);
    ''', {"r_id": get_room_id, "c_id": client_id, "c_in": check_in, "c_out": check_out})

    #подключение услуг
    if service_list:
        get_booking_id = int(pd.read_sql('''
            SELECT MAX(booking_id) AS number_booking
            FROM booking
        ''', conn)['number_booking'].iloc[0])

        for service_id in service_list:
            cur.execute('''
                INSERT INTO costumer_services(booking_id, service_id)
                VALUES 
                    (:b_id, :s_id);
            ''', {"b_id": get_booking_id, "s_id": service_id})
    conn.commit()
