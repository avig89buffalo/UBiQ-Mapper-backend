from .db import db,ObjectId


class Segments(db.Document):
    trip_id = db.ObjectIdField(required=False, default=ObjectId)
    way_id = db.ObjectIdField(required=False, default=ObjectId)
    elevation = db.StringField(required=False)
    node_id = db.ObjectIdField(required=False, default=ObjectId)