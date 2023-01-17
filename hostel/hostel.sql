-- Таблица: ТИП_КОМНАТЫ
DROP TABLE IF EXISTS room_type;

CREATE TABLE IF NOT EXISTS room_type(
    type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name VARCHAR(45) NOT NULL,
    price INTEGER NOT NULL
);
-- Заполнение: ТИП_КОМНАТЫ
INSERT INTO room_type(type_name, price)
VALUES
    ('Одноместный', 500),
    ('Двухместный', 975),
    ('Семейный', 1800),
    ('Вип', 3962),
    ('Бизнес', 6000);


-- Таблица: ОПИСАНИЕ_НОМЕРА
DROP TABLE IF EXISTS room_description;

CREATE TABLE IF NOT EXISTS room_description(
    description_id INTEGER PRIMARY KEY AUTOINCREMENT,
    description VARCHAR(45) NOT NULL,
    detailed_description VARCHAR(90) NOT NULL
);
-- Заполнение: ОПИСАНИЕ_НОМЕРА
INSERT INTO room_description(description, detailed_description)
VALUES
    ('С видом на море',
        'Из этой комнаты открывается прекрасный вид на морские пейзажи.'),
    ('С видом на город',
        'Из окон комнаты открывается удивительный вид на городской ландшафт.'),
    ('С видом на лес',
        'Если у вас есть желание отдохнуть от городской суеты, то данная комната отлично вам подходит.');

-- Таблица: КОМНАТА
DROP TABLE IF EXISTS room;

CREATE TABLE IF NOT EXISTS room(
    room_id INTEGER PRIMARY KEY,
    type_id INTEGER NOT NULL,
    description_id  INTEGER NOT NULL,
    FOREIGN KEY (type_id) REFERENCES room_type (type_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (description_id) REFERENCES room_description (description_id) ON DELETE RESTRICT ON UPDATE CASCADE
);
-- Заполнение: КОМНАТА
INSERT INTO room(room_id, type_id, description_id)
VALUES
     (101, 1, 1),
     (102, 1, 1),
     (103, 1, 2),
     (104, 1, 3),
     (105, 1, 3),
     (106, 2, 1),
     (107, 2, 2),
     (108, 2, 2),
     (109, 2, 2),
     (110, 2, 3),
     (201, 3, 1),
     (202, 3, 1),
     (203, 3, 1),
     (204, 3, 1),
     (205, 3, 2),
     (206, 3, 2),
     (207, 3, 3),
     (208, 3, 3),
     (209, 3, 3),
     (210, 3, 3),
     (301, 4, 1),
     (302, 4, 2),
     (303, 4, 3),
     (304, 5, 1),
     (305, 5, 2);


-- Таблица: КЛИЕНТ
DROP TABLE IF EXISTS client;

CREATE TABLE IF NOT EXISTS client(
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name VARCHAR(45) NOT NULL,
    passport VARCHAR(10) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL UNIQUE
);
-- Заполнение: КЛИЕНТ
INSERT INTO client(client_name, passport, phone)
VALUES
    ('Петров И.В.', '1010234501', '8-999-251-18-01'),
    ('Иванов Ф.П.', '1010181902', '8-999-251-18-02'),
    ('Абрамов В.С.', '1010202003', '8-999-251-18-03'),
    ('Сергеева В.К.', '1010373304', '8-999-251-18-04'),
    ('Кондратьев А.Д.', '1010111105', '8-999-251-18-05'),
    ('Селезнёв Э.Т.', '1011363304', '8-800-555-35-35'),
    ('Румянцев Д.В.', '1021567899', '8-999-251-18-06'),
    ('Хлебников Р.И.', '1307157842', '8-999-251-18-07'),
    ('Кружкина И.В.', '1625364964', '8-999-251-18-08'),
    ('Кубышкин В.В.', '7221431702', '8-999-251-18-09'),
    ('Крошкина Н.С.', '4518921836', '8-999-251-18-10'),
    ('Малышкин С.Э.', '9617221136', '8-999-251-18-11'),
    ('Глинцов М.А.', '1010202004', '8-999-251-18-12'),
    ('Мышкина А.М', '1010202005', '8-999-251-18-13'),
    ('Сычев К.Л.', '1010202006', '8-999-251-18-14'),
    ('Шпак Г.Ш.', '1010202007', '8-999-251-18-15');


-- Таблица: СТАТУС_КОМНАТЫ
DROP TABLE IF EXISTS status_room;

CREATE TABLE IF NOT EXISTS status_room(
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    status_name VARCHAR(20) NOT NULL
);
-- Заполнение: СТАТУС_КОМНАТЫ
INSERT INTO status_room(status_name)
VALUES
    ('забронирована'),
    ('отменена');


-- Таблица: БРОНИРОВАНИЕ
DROP TABLE IF EXISTS booking;

CREATE TABLE IF NOT EXISTS booking(
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL,
    date_check_in DATE NOT NULL,
    date_check_out DATE NOT NULL,
    FOREIGN KEY (room_id) REFERENCES room (room_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (client_id) REFERENCES client (client_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (status_id) REFERENCES status_room (status_id) ON DELETE RESTRICT ON UPDATE CASCADE
);
-- Заполнение: БРОНИРОВАНИЕ
INSERT INTO booking(room_id, client_id, status_id, date_check_in, date_check_out)
VALUES
    (101, 1, 2, '2022-10-01', '2022-10-18'),
    (102, 1, 1, '2022-10-01', '2022-10-21'),
    (103, 2, 1, '2022-10-04', '2022-10-15'),
    (104, 3, 1, '2022-10-01', '2022-10-04'),
    (105, 10, 1, '2022-10-01', '2022-10-03'),
    (107, 9, 2, '2022-10-12', '2022-10-21'),
    (109, 9, 1, '2022-10-10', '2022-10-18'),
    (101, 8, 1, '2022-10-18', '2022-11-09'),
    (301, 7, 1, '2022-10-01', '2022-10-05'),
    (305, 6, 1, '2022-10-01', '2022-10-05'),
    (106, 4, 1, '2022-09-30', '2022-10-07'),
    (108, 5, 1, '2022-09-30', '2022-10-07'),
    (110, 6, 1, '2022-09-30', '2022-10-07'),
    (201, 16, 2, '2022-10-07', '2022-10-21'),
    (201, 15, 1, '2022-10-05', '2022-10-21'),
    (202, 14, 1, '2022-10-02', '2022-10-18'),
    (203, 13, 1, '2022-10-06', '2022-10-22'),
    (204, 12, 1, '2022-10-03', '2022-10-19'),
    (205, 11, 1, '2022-10-05', '2022-10-21'),
    (206, 9, 1, '2022-11-02', '2022-12-04'),
    (101, 3, 1, '2022-11-10', '2022-11-27'),
    (207, 4, 2, '2022-10-15', '2022-11-21'),
    (208, 1, 1, '2022-10-15', '2022-10-21'),
    (209, 4, 1, '2022-10-15', '2022-10-31'),
    (210, 2, 1, '2022-10-01', '2022-10-21'),
    (210, 3, 1, '2022-12-29', '2023-01-11'),
    (301, 8, 1, '2022-12-28', '2023-01-11'),
    (302, 9, 1, '2022-12-31', '2023-01-15'),
    (303, 1, 1, '2022-12-29', '2023-01-01'),
    (304, 5, 1, '2022-12-30', '2023-01-07'),
    (305, 7, 1, '2022-12-28', '2023-01-05');


-- Таблица: УСЛУГА
DROP TABLE IF EXISTS service;

CREATE TABLE IF NOT EXISTS service (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name VARCHAR(45) NOT NULL,
    price INTEGER NOT NULL
);
-- Заполнение: УСЛУГА
INSERT INTO service(service_name, price)
VALUES
    ('Завтрак в постель', 205),
    ('Уборка в комнате', 350),
    ('Экскурсия 1', 400),
    ('Экскурсия 2', 580),
    ('Экскурсия 3', 750),
    ('Шведский стол', 650),
    ('Мороженое', 100);


-- Таблица: УСЛУГА_ДЛЯ_КЛИЕНТА
DROP TABLE IF EXISTS costumer_services;

CREATE TABLE IF NOT EXISTS costumer_services (
    costumer_services_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES booking (booking_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (service_id) REFERENCES service (service_id) ON DELETE RESTRICT ON UPDATE CASCADE
);
-- Заполнение УСЛУГА_ДЛЯ_КЛИЕНТА
INSERT INTO costumer_services(booking_id, service_id)
VALUES
    (1, 4),
    (2, 5),
    (5, 1),
    (5, 2),
    (5, 3),
    (5, 4),
    (5, 5),
    (5, 6),
    (5, 7),
    (9, 1),
    (9, 6),
    (9, 7),
    (10, 1),
    (10, 2),
    (10, 3),
    (10, 5),
    (10, 7),
    (26, 1),
    (26, 2),
    (26, 3),
    (26, 4),
    (26, 5),
    (26, 6),
    (26, 7);