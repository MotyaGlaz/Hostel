import sqlite3


def get_db_connection():
    return sqlite3.connect('hostel.sqlite')


def get_year(str_date):
    return int(str_date[:4])


def get_month(str_date):
    return int(str_date[5:7])


def get_day(str_date):
    return int(str_date[8:10])


rooms_status = ['Оконченное бронирование', 'Предстоящее бронирование',
                'Активное бронирование', 'Отменённое бронирование']
