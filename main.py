from pony.orm import *

from models import db
from flask import Flask
from pony.flask import Pony


app = Flask(__name__)
Pony(app)

from views import *

@db_session
def generate_db_data():
    if db.StageType.select().first() is None:
        db.StageType(name='Lecture')
        db.StageType(name='Presentation')
        db.StageType(name='Master Class')
        db.StageType(name='Coffee break')
    if db.Organisator.select().first() is None:
        db.Organisator(inn=5123, name='Prime Event')
        db.Organisator(inn=3143, name='Showcompany')
        db.Organisator(inn=1787, name='Promofabrika')
        db.Organisator(inn=7589, name='Grand Premier')
    if db.Place.select().first() is None:
        place_a2 = db.Place(name='A2 Concert Hall')
        place_air = db.Place(name='Club AIR')
        place_ph = db.Place(name='BC Phoenix')
        place_morskaya = db.Place(name='BC Morskaya')
    if db.Auditory.select().first() is None:
        db.Auditory(number=1, capacity=100, place=place_a2)
        db.Auditory(number=2, capacity=20, place=place_a2)
        db.Auditory(number=3, capacity=5, place=place_a2)

        db.Auditory(number=1, capacity=120, place=place_air)
        db.Auditory(number=2, capacity=10, place=place_air)
        db.Auditory(number=3, capacity=10, place=place_air)

        db.Auditory(number=7, capacity=24, place=place_ph)
        db.Auditory(number=15, capacity=48, place=place_ph)
        db.Auditory(number=33, capacity=96, place=place_ph)

        db.Auditory(number=101, capacity=64, place=place_morskaya)
        db.Auditory(number=1001, capacity=128, place=place_morskaya)
        db.Auditory(number=11, capacity=256, place=place_morskaya)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


generate_db_data()
