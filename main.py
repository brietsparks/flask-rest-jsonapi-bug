from flask import Flask
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields
from flask_migrate import Migrate

# Create the Flask application and the Flask-SQLAlchemy object.
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PAGE_SIZE'] = 30
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

event_person = db.Table(
    'event_person',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

# Create model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    events = db.relationship('Event', secondary=event_person, backref='persons')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

# Create the database.
db.create_all()

# Create schema
class PersonSchema(Schema):
    class Meta:
        type_ = 'person'
        self_view = 'person_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'person_list'

    id = fields.Integer(as_string=True, dump_only=True)
    name = fields.Str()

    events = Relationship(self_view='person_events',
                          self_view_kwargs={'id': '<id>'},
                          related_view='event_list',
                          related_view_kwargs={'id': '<id>'},
                          many=True,
                          schema='EventSchema',
                          type_='events')


class EventSchema(Schema):
    class Meta:
        type_ = 'event'
        self_view = 'event_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'event_list'

    id = fields.Integer(as_string=True, dump_only=True)
    name = fields.Str()


# Create resource managers
class PersonList(ResourceList):
    schema = PersonSchema
    data_layer = {'session': db.session,
                  'model': Person}

class PersonDetail(ResourceDetail):
    schema = PersonSchema
    data_layer = {'session': db.session,
                  'model': Person}

class PersonRelationship(ResourceRelationship):
    schema = PersonSchema
    data_layer = {'session': db.session,
                  'model': Person}

class EventList(ResourceList):
    schema = EventSchema
    data_layer = {'session': db.session,
                  'model': Event}

class EventDetail(ResourceDetail):
    schema = EventSchema
    data_layer = {'session': db.session,
                  'model': Event}

class EventRelationship(ResourceRelationship):
    schema = EventSchema
    data_layer = {'session': db.session,
                  'model': Event}

# Create the API object
api = Api(app)
api.route(PersonList, 'person_list', '/persons')
api.route(PersonDetail, 'person_detail', '/persons/<int:id>')
api.route(PersonRelationship, 'person_events', '/persons/<int:id>/relationships/events')
api.route(EventList, 'event_list', '/events')
api.route(EventDetail, 'event_detail', '/events/<int:id>')


# Start the flask loop
if __name__ == '__main__':
    app.run()