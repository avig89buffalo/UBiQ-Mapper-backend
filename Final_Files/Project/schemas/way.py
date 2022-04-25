from .db import db,ObjectId

class Way(db.Document):
    city = db.StringField( required=False)
    node_ids = db.ListField(required=False)
    way_id = db.FloatField(required=False)