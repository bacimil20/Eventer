from datetime import datetime
from datetime import time
from flask import render_template, request, url_for, redirect
from flask.json import jsonify
from pony.orm import *
from flask_login import login_required, login_user, logout_user, current_user

from main import app
from models import db


@app.route('/test')
def test():
    return 'test'


@app.route('/login', methods=['GET', 'POST'])
@db_session
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('login.html', error=False)
    else:
        data = dict(request.form)
        customer = db.Customer.get(email=data['email'])
        if customer:
            if customer.check_password(data['password']):
                login_user(customer)
                return redirect('/')
        return render_template('login.html', error=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/')
@login_required
@db_session
def home():
    events = list(select(e for e in db.Event if e.customer == current_user)[:])
    return render_template('home.html', events=events)


@app.route('/create_event')
@login_required
@db_session
def create_event_form():
    organisators = list(select(org for org in db.Organisator)[:])
    places = list(select(place for place in db.Place)[:])
    for place in places:
        place.capacity = sum(list(select(a.capacity for a in place.auditorys)))
    return render_template('create_event.html', organisators=organisators, places=places)


@app.route('/events/<event_id>', methods=['DELETE'])
@login_required
@db_session
def event_delete(event_id):
    delete(t for t in db.Ticket if event==event_id)
    db.Event[event_id].delete()
    return 'ok'


@app.route('/events', methods=['POST'])
@login_required
@db_session
def event_create():
    data = dict(request.form)
    ticket_cost = data.pop('ticket_cost')
    tickets_quantity = int(data.pop('tickets_quantity'))
    data['date_start'] = datetime.strptime(data['date_start'], '%d/%m/%Y')
    data['date_end'] = datetime.strptime(data['date_end'], '%d/%m/%Y')
    data['customer'] = current_user
    event = db.Event(**data)
    for i in range(tickets_quantity):
        db.Ticket(event=event, price=ticket_cost)
    return redirect('/')


@app.route('/stage_types', methods=['POST', 'GET'])
@login_required
@db_session
def stage_type_list():
    if request.method == 'GET':
        response = []
        stage_types = list(select(st for st in db.StageType)[:])
        for st in stage_types:
            response.append(st.to_dict())
        return jsonify(response)
    else:
        db.StageType(name=request.form['name'])
        return 'ok'


@app.route('/stages', methods=['POST', 'GET'])
@login_required
@db_session
def stage_create():
    if request.method == 'GET':
        response = []
        stage_types = list(select(st for st in db.Stage)[:])
        for st in stage_types:
            response.append(st.to_dict())
        return jsonify(response)
    else:
        data = dict(request.form)
        data['date'] = datetime.strptime(data['date'], '%d/%m/%Y')
        data['time_start'] = time(*[int(t) for t in data['time_start'].split(':')])
        data['time_end'] = time(*[int(t) for t in data['time_end'].split(':')])
        db.Stage(**data)
        return redirect('/events/{}'.format(data['event']))


@app.route('/events/<event_id>')
@login_required
def event(event_id):
    event = db.Event[event_id]
    return render_template('event.html', event=event)


@app.route('/events/<event_id>/create_stage')
@login_required
def create_stage(event_id):
    event = db.Event[event_id]
    stage_types = list(select(st for st in db.StageType)[:])
    auditories = list(select(a for a in db.Auditory if a.place==event.place)[:])
    return render_template('create_stage.html', event=event, stage_types=stage_types, auditories=auditories)


@app.route('/events/check_quantity', methods=['POST'])
@login_required
@db_session
def check_quantity():
    data = dict(request.form)
    place = db.Place[data['place']]
    place_max_capacity = sum(list(select(a.capacity for a in place.auditorys)))
    if place_max_capacity < int(data['ticket_quantity']):
        return 'not ok', 400
    return 'ok'



@app.route('/create_customer', methods=['POST'])
@db_session
def create_customer():
    data = dict(request.form)
    errors = []
    customer = db.Customer.get(email=data['email'])
    if customer:
        errors.append('Пользователь с таким email уже существует')
    customer = db.Customer.get(inn=data['inn'])
    if customer:
        errors.append('Пользователь с таким ИНН уже существует')
    customer = db.Customer.get(phone_number=data['phone_number'])
    if customer:
        errors.append('Пользователь с таким номером телефона уже существует')
    if errors:
        return render_template('register.html', errors=errors)
    customer = db.Customer(**data)
    customer.set_password(data['password'])
    commit()
    login_user(customer)
    return redirect('/')


@app.route('/register')
def register():
    return render_template('register.html', errors=[])
