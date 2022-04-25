from .db import db,ObjectId
from schemas.segments import Segments

class segmentElevations(db.Document):
    segment_id = db.FloatField(required=False)
    location = db.PointField(required=False)
    distance = db.FloatField(required=False)
    elevation = db.FloatField(required=False)