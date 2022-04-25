from .db import db,ObjectId

class Trips(db.Document):
    trip_id = db.StringField(required=False)
    node_ids = db.ListField(required=False)
    # way_id = db.ObjectIdField(required=False, default=ObjectId)
    segment_ids = db.ListField(required=False)
    city = db.StringField(required=False)