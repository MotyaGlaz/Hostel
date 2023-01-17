import pandas as pd
import sqlite3


con = sqlite3.connect('../hostel.sqlite')


def create_Hostel():
    f_damp = open('hostel.sql', 'r', encoding='utf-8-sig')
    damp = f_damp.read()
    f_damp.close()

    con.executescript(damp)
    con.commit()


# Запрос: вывести список номеров с их типом и ценой, которые ниже заданной цены
# Сортировка по типу в алфавитном порядке
def queryRoomInformation():
    max_price = int(input('Введите максимальную цену: '))

    data_frame = pd.read_sql('''
        SELECT 
            room_id AS Комната, 
            type_name AS Тип, 
            price AS Цена
        FROM room
            INNER JOIN room_type USING (type_id)
        WHERE price < :m_price
        ORDER BY type_name
    ''', con, params={"m_price": max_price})

    print(data_frame)


# Запрос: вывести активных проживающих (с инф-ей о бронировании) на сегодняшний день
# Сортировка по имени клиента
def queryCurrentResident():
    data_frame = pd.read_sql('''
        SELECT 
            client_name AS Клиент, 
            room_id AS Комната, 
            date_check_in AS Заселение, 
            date_check_out AS Выселение
        FROM booking
            LEFT JOIN client USING (client_id)
        WHERE status_id = 1 AND
            ((date('now') >= date_check_in AND date('now') <= date_check_out)
                OR date_check_out IS NULL)
        ORDER BY client_name
    ''', con)

    print(data_frame)


# Запрос: вывести список свободных номеров (комната и её тип) на промежуток времени (даты)
def queryFreeRooms():
    check_in = '2022-10-22'# input('Введите дату начала бронирования (пример 2000-01-01): ')
    check_out = '2022-10-31'# input('Введите дату конца бронирования: ')

    data_frame = pd.read_sql('''
        SELECT room_id, type_name
        FROM room
            INNER JOIN room_type USING (type_id)
        WHERE room_id NOT IN (SELECT room_id
                              FROM booking
                              WHERE date_check_out IS NULL OR
                                    (date_check_out >= :c_in AND date_check_in <= :c_in) OR 
                                    (date_check_in <= :c_out AND date_check_out >= :c_out) OR
                                    (date_check_in >= :c_in AND date_check_out <= :c_out))
    ''', con, params={"c_in": check_in, "c_out": check_out})

    print(data_frame)


# Запрос: Вывести свободные комнаты (номер и тип) на сегодняшний день
def queryFreeRoomsNow():
    data_frame = pd.read_sql('''
     SELECT room_id, type_name
        FROM room
            INNER JOIN room_type USING (type_id)
        WHERE room_id NOT IN (SELECT room_id
                              FROM booking
                              WHERE date_check_out IS NULL OR
                                    (date_check_out >= date('now') AND date_check_in <= date('now')))
    ''', con)

    print(data_frame)


# Запрос: выставить счёт конкретному клиенту
def queryCustomerAccount():
    customer = 'Кубышкин В.В.' #input('Введите имя проживающего (инициалы с большой буквы без пробелов): ')

    data_frame = pd.read_sql('''
        SELECT
            booking_id AS Бронь,
            IIF(date_check_out NOT NULL,
                room_type.price * CAST((JULIANDAY(date_check_out) - JULIANDAY(date_check_in) + 1) AS INTEGER) +  SUM(service.price),
                room_type.price * CAST((JULIANDAY(date('now')) - JULIANDAY(date_check_in) + 1) AS INTEGER) +  SUM(service.price)
            )  AS Цена
            FROM costumer_services
                INNER JOIN service USING (service_id)
                INNER JOIN booking USING (booking_id)
                INNER JOIN room USING (room_id)
                INNER JOIN room_type USING (type_id)
            INNER JOIN client USING (client_id)
            WHERE status_id = 1 AND date('now') > date_check_in
            AND (date('now') <= date_check_out OR date_check_out IS NULL)
            AND client.client_name = :cust
            GROUP BY booking_id
    ''', con, params={"cust": customer})

    print(data_frame)


# Запрос: реализовать акцию — скидка 25% на фулл прайс на 1 день для каждого типа номера
# Вывести тип комнаты и цену акции
def queryFullPrice():
    data_frame = pd.read_sql('''
        SELECT
            type_name AS Тип,
            (price +
                ROUND((SELECT SUM(price) FROM service)*0.75, 2)
            ) AS Цена
        FROM room_type
    ''', con)

    print(data_frame)


# Запрос: расчёт прибыли отеля с учётом занятости всех комнат за 1 день
# Вывести тип и прибыль
def queryFullProfit():
    data_frame = pd.read_sql('''
        SELECT
            type_name,
            (price*(SELECT COUNT(room_id) FROM room GROUP BY type_id)) AS price
        FROM room_type
    ''', con)

    print(data_frame)


# Запрос: отменить бронирование (указать бронь)
def queryUpdateStatusBooking():
    booking = int(input('Введите номер брони: '))

    con.execute('''
        UPDATE booking
        SET status_id = 2 -- была 1
        WHERE  booking_id = :b_id
    ''', {"b_id": booking})

    con.commit()


# Запрос: изменить цену заданной услуги
def queryChangeServicePrice():
    name_service = 'Мороженое' # input('Введите название услуги(с большой буквы): ')

    con.execute('''
        UPDATE service
        SET price = price*0.9 -- нужно /0.9
        WHERE service_name = :n_service
    ''', {"n_service": name_service})

    con.commit()


# =====____=====
# create_Hostel()
# queryRoomInformation()
# queryCurrentResident()
# --
# queryFreeRooms()
# queryFreeRoomsNow()
# ---
# queryCustomerAccount()
# queryFullPrice()
# queryFullProfit()
# queryUpdateStatusBooking()
# queryChangeServicePrice()
