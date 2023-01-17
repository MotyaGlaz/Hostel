from app import app
from utils import get_db_connection, get_year, get_month, get_day
from flask import render_template, request, session
from models.index_model import get_type_room, get_description_room, get_available_type, get_service, get_client, \
    make_booking
from datetime import date
from dateutil.relativedelta import relativedelta


@app.route('/', methods=['get', 'post'])
def index():
    conn = get_db_connection()
    df_type_room = get_type_room(conn)
    df_description_room = get_description_room(conn)
    df_service = get_service(conn)
    df_available_type = []
    df_client = get_client(conn)

    current_day = date.today()

    # доделать проверку дат (при вводе начала менялся и конец на +1)
    if request.values.get('find_room'):
        session['date_check_in'] = request.values.get('date_check_in')
        session['date_check_out'] = request.values.get('date_check_out')
        session['room_types'] = request.values.getlist('select_types')
        session['room_descriptions'] = request.values.getlist('select_descriptions')
        if session['room_types']:
            df_available_type = get_available_type(conn, session['date_check_in'], session['date_check_out'],
                                                   session['room_types'], session['room_descriptions'])
        service_list = []

    elif request.values.get('make_booking'):
        service_list = request.values.getlist('select_service')
        session['type_id'] = request.values.get('type_id')
        session['description_id'] = request.values.get('description_id')
        if session['client_id'] == '':
            session['client_id'] = int(request.values.get('client_id'))
        make_booking(conn, session['date_check_in'], session['date_check_out'], session['type_id'],
                     session['description_id'], session['client_id'], service_list)


    elif request.values.get('authorization'):
        session['client_id'] = int(request.values.get('select_client'))
        service_list = []

        date_check_in = session['date_check_in']
        date_check_out = session['date_check_out']
        min_date = session['min_date']

    elif request.values.get('exit'):
        session['client_id'] = ''
        service_list = []


    # переход от страницы 'my_booking' к странице 'index'
    elif request.values.get('client'):
        session['client_id'] = request.values.get('client')
        service_list = []


    else:
        session['date_check_in'] = date.today()
        session['date_check_out'] = date.today() + relativedelta(days=1)
        session['min_date'] = date(get_year(str(session['date_check_in'])), get_month(str(session['date_check_in'])),
                        get_day(str(session['date_check_in']))) + relativedelta(days=1)

        session['room_types'] = []
        session['room_descriptions'] = []
        service_list = []

        session['type_id'] = ''
        session['description_id'] = ''
        session['client_id'] = ''

    # рендеринг странички
    html = render_template(
        'index.html',
        check_in=session['date_check_in'],
        check_out=session['date_check_out'],
        min_date=session['min_date'],
        current_day=current_day,

        df_type_room=df_type_room,
        df_description_room=df_description_room,
        df_service=df_service,
        df_available_type=df_available_type,
        df_client=df_client,

        room_type_list=session['room_types'],
        room_description_list= session['room_descriptions'],
        service_list=service_list,

        type_id=session['type_id'],
        description_id=session['description_id'],
        client_id= session['client_id'],

        len=len,
        str=str,
        int=int
    )
    return html
