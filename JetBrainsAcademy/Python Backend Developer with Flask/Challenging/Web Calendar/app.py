from datetime import date
from flask import abort, Flask, request
from flask_restful import inputs, reqparse, Api, Resource, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import sys

app = Flask(__name__)

api = Api(app)

# write your code here
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'
db.init_app(app)


class Event(db.Model):
    __tablename__ = "Event"
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=True)
    date = db.Column(db.Date, nullable=True)


get_resource_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.String
}

post_resource_fields = {
    'event': fields.String,
    'date': fields.String,
    'message': fields.String
}

delete_resource_fields = {
    'message': fields.String
}

with app.app_context():
    db.drop_all()
    db.create_all()

parser = reqparse.RequestParser()
parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)
parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)


class TodayEventResource(Resource):
    @marshal_with(get_resource_fields)
    def get(self):
        result = [row for row in Event.query.filter(Event.date == date.today()).all()]
        return result


api.add_resource(TodayEventResource, '/event/today')


class EventResource(Resource):
    @marshal_with(get_resource_fields)
    def get(self, id=None):
        args = request.args
        start_time = args.get('start_time', None)
        end_time = args.get('end_time', None)

        if start_time is None and end_time is None:
            if id is None:
                result = [row for row in Event.query.all()]
                return result

            result = Event.query.get(id)
            if result is None:
                abort(404, "The event doesn't exist!")
            else:
                return result
        else:
            start_date = date.fromisoformat(start_time)
            end_date = date.fromisoformat(end_time)
            result = Event.query.filter(and_(Event.date >= start_date,
                                             Event.date <= end_date))

            if result is None:
                abort(404, "The event doesn't exist!")
            else:
                return [row for row in result]

    @marshal_with(post_resource_fields)
    def post(self):
        args = parser.parse_args()
        event = Event(event=args['event'], date=args['date'].date())
        db.session.add(event)
        db.session.commit()

        response = {
            "message": "The event has been added!",
            "event": args['event'],
            "date": str(args['date'].date())
        }
        return response

    @marshal_with(delete_resource_fields)
    def delete(self, id=None):
        if id is None:
            abort(404, "The event doesn't exist!")

        the_event = Event.query.filter(Event.id == id)

        if db.session.query(the_event.exists()).scalar():
            the_event.delete()
            db.session.commit()
            response = {
                "message": "The event has been deleted!"
            }
            return response

        abort(404, "The event doesn't exist!")


api.add_resource(EventResource, '/event', '/event/<int:id>')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(port=8080)
