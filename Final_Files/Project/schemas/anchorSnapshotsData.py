from .db import db,ObjectId
import datetime

class AnchorSnapshotsData(db.Document):
    trip_id = db.StringField(required=False)
    timestamp = db.FloatField()
    value = db.FloatField()