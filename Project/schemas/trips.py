from .db import db,ObjectId

class Trips(db.Document):
    node_id = db.ObjectIdField(required=False, default=ObjectId)
    way_id = db.ObjectIdField(required=False, default=ObjectId)
    city = db.StringField(required=False)
    