from datetime import datetime
from flask import render_template, request, url_for, redirect
from flask.json import jsonify
from pony.orm import *

from main import app
from models import db


@app.route('/test')
def test():
    return 'test'


@app.route('/')
@db_session
def home():
    events = list(select(e for e in db.Event)[:])
    return render_template('home.html', events=events)


@app.route('/create_event')
@db_session
def create_event_form():
    organisators = list(select(org for org in db.Organisator)[:])
    places = list(select(place for place in db.Place)[:])
    return render_template('create_event.html', organisators=organisators, places=places)


@app.route('/events/<event_id>', methods=['DELETE'])
@db_session
def event_delete(event_id):
    delete(t for t in db.Ticket if event==event_id)
    db.Event[event_id].delete()
    return 'ok'


@app.route('/events', methods=['POST'])
@db_session
def event_create():
    data = dict(request.form)
    ticket_cost = data.pop('ticket_cost')
    tickets_quantity = int(data.pop('tickets_quantity'))
    data['date_start'] = datetime.strptime(data['date_start'], '%d/%m/%Y')
    data['date_end'] = datetime.strptime(data['date_end'], '%d/%m/%Y')
    event = db.Event(**data)
    for i in range(tickets_quantity):
        db.Ticket(event=event, price=ticket_cost)
    return redirect('/')


@app.route('/stage_types', methods=['POST', 'GET'])
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
        data['date_start'] = datetime.strptime(data['date_start'], '%d/%m/%Y')
        data['date_end'] = datetime.strptime(data['date_end'], '%d/%m/%Y')
        db.Stage(**data)
        return redirect('/events/{}'.format(data['event']))


@app.route('/events/<event_id>')
def event(event_id):
    event = db.Event[event_id]
    return render_template('event.html', event=event)


@app.route('/events/<event_id>/create_stage')
def create_stage(event_id):
    event = db.Event[event_id]
    stage_types = list(select(st for st in db.StageType)[:])
    auditories = list(select(a for a in db.Auditory if a.place==event.place)[:])
    return render_template('create_stage.html', event=event, stage_types=stage_types, auditories=auditories)


@app.route('/events/check_quantity', methods=['POST'])
@db_session
def check_quantity():
    data = dict(request.form)
    place = db.Place[data['place']]
    place_max_capacity = sum(list(select(a.capacity for a in place.auditorys)))
    if place_max_capacity < int(data['ticket_quantity']):
        return 'not ok', 400
    return 'ok'
