from .db import db,ObjectId

class Nodes(db.Document):
    latitude = db.FloatField(required=False)
    longitude = db.FloatField(required=False)