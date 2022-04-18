from .db import db,ObjectId
from schemas.segments import Segments

class segmentElevations(db.Document):
    segment_id = db.FloatField(required=True)
    location = db.PointField(required=True)
    distance = db.FloatField(required=True)
    elevation = db.FloatField(required=True)