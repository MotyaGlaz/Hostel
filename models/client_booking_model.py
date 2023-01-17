import pandas as pd


def get_booking_client(conn, client_id, current_day):
    booking = pd.read_sql('''
        SELECT
            booking_id, 
            
            room_id,
            description,
            detailed_description,
            type_id,
            type_name,
            price AS price_booking,
            price * CAST((JULIANDAY(date_check_out) - JULIANDAY(date_check_in) + 1) AS INTEGER) AS full_price,
            
            client_id,
            IIF(status_id = 1, 
                IIF(date_check_out < :c_day, 'Оконченное бронирование', 
                    IIF(:c_day < date_check_in, 'Предстоящее бронирование', 'Активное бронирование')), 
                'Отменённое бронирование') AS status, 
            date_check_in, 
            date_check_out,
            IIF(:c_day < date_check_in, TRUE, FALSE) AS is_change_booking,
            IIF(:c_day >= date_check_in AND :c_day <= date_check_out, TRUE, FALSE) AS is_change_service
        FROM booking
            INNER JOIN room USING (room_id)
            INNER JOIN room_description USING (description_id)
            INNER JOIN room_type USING (type_id)
        WHERE client_id = :c_id
    ''', conn, params={"c_id": client_id, "c_day": current_day})

    booking_id_list = [int(b_id) for b_id in booking['booking_id']]
    services = {}
    services_list ={}
    for b_id in booking_id_list:
        services[b_id] = pd.read_sql('''
            SELECT
                costumer_services_id, 
                booking_id, 
                service_id, 
                service_name, 
                price AS price_service
            FROM costumer_services
                INNER JOIN service USING (service_id)
            WHERE booking_id = :b_id
        ''', conn, params={"b_id": b_id})
        list = []
        for i in range(len(services[b_id])):
            list.append(services[b_id]['service_id'].iloc[i])
        services_list[b_id] = list

    return {"booking": booking, "services": services, "services_list": services_list}


def delete_booking(conn, booking_id):
    cur = conn.cursor()

    cur.execute('''
        UPDATE booking
        SET status_id = 2
        WHERE booking_id = :b_id
    ''', {"b_id": booking_id})

    conn.commit()


def change_service(conn, booking_id, service_list):

    df_service_booking = pd.read_sql('''
        SELECT service_id
        FROM costumer_services
        WHERE booking_id = :b_id
    ''', conn, params={"b_id": booking_id})

    pre_service_list = []
    if len(df_service_booking) > 0:
        for i in range(len(df_service_booking)):
            pre_service_list.append(str(df_service_booking.loc[i, "service_id"]))

    # проверка на изменение сервисов
    if pre_service_list != service_list:
        cur = conn.cursor()
        delete_service_list = ['1', '2', '3', '4', '5', '6', '7']

        # убираем из удаления то, что выбрал пользователь
        if service_list:
            for i in service_list:
                delete_service_list.remove(i)

            # убираем из удаления то, чего нет ни в прошло ни в нынешнем
            if pre_service_list:
                for i in delete_service_list:
                    if i not in pre_service_list and i not in service_list:
                        delete_service_list.remove(i)

        # если список удаления не пуст
        if delete_service_list:
            cur.execute(f'''
                DELETE FROM costumer_services
                WHERE booking_id = :b_id AND service_id in ({str(delete_service_list).strip('[]')})
            ''', {"b_id": booking_id})

        # если список выбранного не пуст
        if service_list:
            for i in service_list:
                if i not in pre_service_list:
                    cur.execute('''
                        INSERT INTO costumer_services(booking_id, service_id)
                        VALUES
                            (:b_id, :s_id)
                    ''', {"b_id": booking_id, "s_id": i})
        conn.commit()
