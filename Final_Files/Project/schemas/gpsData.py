from .db import db,ObjectId
import datetime

class GpsData(db.Document):
    trip_id = db.StringField(required=False)
    timestamp = db.FloatField()
    system_timestamp = db.FloatField()
    latitude = db.FloatField(required=False)
    longitude = db.FloatField(required=False)
    map_matched_latitude = db.FloatField()
    map_matched_longitude = db.FloatField()
    velocity = db.FloatField()
    acc = db.FloatField()
    bearing = db.FloatField()
    bad_data = db.FloatField()
    city = db.StringField(required=False)
    nearest_node = db.FloatField()