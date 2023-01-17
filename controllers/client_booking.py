from app import app
from utils import get_db_connection
from flask import  render_template, request, session
from models.client_booking_model import get_booking_client, delete_booking, change_service
from models.index_model import get_client, get_service
from datetime import date
from dateutil.relativedelta import relativedelta


@app.route('/client_booking', methods=['get', 'post'])
def client_booking():
    current_day = date.today()
    conn = get_db_connection()
    df_client = get_client(conn)
    df_service = get_service(conn)

    if request.values.get('client'):
        session['client_id'] = int(request.values.get('client'))
        client_id = session['client_id']

    # отмена бронирования
    elif request.values.get('delete_booking'):
        client_id = session['client_id']
        booking_id = request.values.get('booking_id')
        delete_booking(conn, booking_id)

    # изменение списка услуг
    elif request.values.get('change_service'):
        client_id = session['client_id']
        booking_id = int(request.values.get('booking_id'))
        service_list = request.values.getlist('select_service')
        change_service(conn, booking_id, service_list)

    else:
        client_id = session['client_id']

    df_booking = get_booking_client(conn, client_id, current_day)["booking"]
    df_booking_services = get_booking_client(conn, client_id, current_day)["services"]
    service_list = get_booking_client(conn, client_id, current_day)["services_list"]


    html = render_template(
        'client_booking.html',
        current_day=current_day,

        df_client=df_client,
        df_service=df_service,
        df_booking=df_booking,
        df_booking_services=df_booking_services,

        client_id=client_id,
        service_list=service_list,

        len=len,
        str=str,
        int=int
    )
    return html
