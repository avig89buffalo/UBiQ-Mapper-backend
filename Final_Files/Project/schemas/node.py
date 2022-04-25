from .db import db,ObjectId
from schemas.segments import Segments

class Nodes(db.Document):
    node_id = db.FloatField(required=False)
    # latitude = db.FloatField(required=True)
    # longitude = db.FloatField(required=True)
    location = db.PointField()
    city = db.StringField(required=False)
    segment_id = db.StringField(required=False)