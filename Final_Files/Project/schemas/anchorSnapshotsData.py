from .db import db,ObjectId
import datetime

class AnchorSnapshotsData(db.Document):
    trip_id = db.StringField(required=True)
    timestamp = db.FloatField()
    value = db.FloatField()