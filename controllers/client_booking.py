from app import app
from utils import get_db_connection, rooms_status
from flask import  render_template, request, session
from models.client_booking_model import get_booking_client, delete_booking, change_service, \
    get_type_room, get_description_room
from models.index_model import get_client, get_service
from datetime import date


@app.route('/client_booking', methods=['get', 'post'])
def client_booking():

    conn = get_db_connection()
    current_day = date.today()

    df_client = get_client(conn)
    df_service = get_service(conn)
    df_type = get_type_room(conn)
    df_description = get_description_room(conn)

    status_room = []
    type_room = []
    description_room = []

    # переход с главной странице (по кнопке, пользователь —> личный кабинет)
    if request.values.get('client'):
        session['client_id'] = int(request.values.get('client'))
        client_id = session['client_id']

        session['status_room'] = status_room
        session['type_room'] = type_room
        session['from_windows'] = description_room


    # сортировка карточек бронирований
    elif request.values.get('sorting'):
        client_id = session['client_id']

        status_room = request.values.getlist('status_room')
        type_room = request.values.getlist('type_room')
        description_room = request.values.getlist('description_room')


    # отмена бронирования
    elif request.values.get('delete_booking'):
        status_room = session['status_room']
        type_room = session['type_room']
        description_room = session['from_windows']
        client_id = session['client_id']

        booking_id = request.values.get('booking_id')
        delete_booking(conn, booking_id)

    # изменение списка услуг для карточки с бронью
    elif request.values.get('change_service'):
        status_room = session['status_room']
        type_room = session['type_room']
        description_room = session['from_windows']
        client_id = session['client_id']

        booking_id = int(request.values.get('booking_id'))
        service_list = request.values.getlist('select_service')
        change_service(conn, booking_id, service_list)

    else:
        status_room = session['status_room']
        type_room = session['type_room']
        description_room = session['from_windows']
        client_id = session['client_id']

    df_booking_client = get_booking_client(conn, client_id, current_day, status_room, type_room, description_room)
    df_booking = df_booking_client["booking"]
    df_booking_services = df_booking_client["services"]
    service_list = df_booking_client["services_list"]


    html = render_template(
        'client_booking.html',
        current_day=current_day,

        # наборы данных
        df_type=df_type,
        df_description=df_description,
        list_status_room=rooms_status,
        df_client=df_client,
        df_service=df_service,
        df_booking=df_booking,
        df_booking_services=df_booking_services,
        df_status_room=rooms_status,

        # ID и списки с ID
        client_id=client_id,
        service_list=service_list,
        type_room_list=type_room,
        status_room_list=status_room,
        description_room_list=description_room,

        # Необходимые функции для макросов
        len=len,
        str=str,
        int=int
    )
    return html
