from .db import db,ObjectId


class Segments(db.Document):
    trip_ids = db.ListField(required=False)
    # way_id = db.ObjectIdField(required=False, default=ObjectId)
    elevation = db.StringField(required=False)
    node_ids = db.ListField(required=True)