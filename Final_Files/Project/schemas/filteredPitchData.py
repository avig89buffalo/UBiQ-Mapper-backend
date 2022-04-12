from .db import db,ObjectId
import datetime

class FilteredPitchData(db.Document):
    trip_id = db.StringField(required=True)
    timestamp = db.FloatField()
    value = db.FloatField()