from datetime import datetime
from datetime import time
from pony.orm import *
from hashlib import sha512

from flask_login import UserMixin

db = Database()


class Organisator(db.Entity):
    id = PrimaryKey(int, auto=True)
    inn = Required(int)
    name = Optional(str)
    phone_number = Optional(str)
    email = Optional(str)
    events = Set('Event')


class Customer(UserMixin, db.Entity):
    id = PrimaryKey(int, auto=True)
    inn = Required(int)
    name = Optional(str)
    phone_number = Optional(str)
    email = Optional(str)
    password = Optional(str)
    events = Set('Event')

    def set_password(self, pwd):
        self.password = sha512(pwd.encode()).hexdigest()

    def check_password(self, pwd):
        return self.password == sha512(pwd.encode()).hexdigest()


class Event(db.Entity):
    id = PrimaryKey(int, auto=True)
    organisator = Required(Organisator)
    name = Optional(str)
    theme = Optional(str)
    date_start = Optional(datetime)
    date_end = Optional(datetime)
    place = Required('Place')
    tickets = Set('Ticket')
    stages = Set('Stage')
    customer = Required('Customer')


class Place(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    country = Optional(str)
    city = Optional(str)
    street = Optional(str)
    house = Optional(str)
    index = Optional(str)
    events = Set(Event)
    auditorys = Set('Auditory')


class Auditory(db.Entity):
    id = PrimaryKey(int, auto=True)
    number = Optional(int)
    capacity = Optional(int)
    place = Required(Place)
    stages = Set('Stage')


class Stage(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    date = Required(datetime)
    time_start = Required(time)
    time_end = Required(time)
    auditory = Required(Auditory)
    event = Required(Event)
    stage_type = Required('StageType')


class Ticket(db.Entity):
    id = PrimaryKey(int, auto=True)
    event = Required(Event)
    seat = Optional(str)
    price = Optional(int)
    owner = Optional('Member')


class Member(db.Entity):
    id = PrimaryKey(int, auto=True)
    fio = Optional(str)
    position = Optional(int)
    phone_number = Optional(str)
    email = Optional(str)
    tickets = Set(Ticket)


class StageType(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    stages = Set(Stage)
