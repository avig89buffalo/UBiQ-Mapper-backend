from .db import db,ObjectId
import datetime

class RawSensorData(db.Document):
    trip_id = db.ObjectIdField(required=False, unique=True)
    gps_lat = db.FloatField(db.FloatField(), required=False)
    gps_long = db.FloatField(db.FloatField(), required=False)
    gps_timeStamp = db.DateTimeField(default=datetime.datetime.utcnow)
    gyro_x = db.FloatField(db.FloatField(), required=False)
    gyro_y = db.FloatField(db.FloatField(), required=False)
    gyro_z = db.FloatField(db.FloatField(), required=False)
    gyro_timeStamp = db.DateTimeField(default=datetime.datetime.utcnow)
    accel_x = db.FloatField(db.FloatField(), required=False)
    accel_y = db.FloatField(db.FloatField(), required=False)
    accel_z = db.FloatField(db.FloatField(), required=False)
    accel_timeStamp = db.DateTimeField(default=datetime.datetime.utcnow)
    grav_x = db.FloatField(db.FloatField(), required=False)
    grav_y = db.FloatField(db.FloatField(), required=False)
    grav_z = db.FloatField(db.FloatField(), required=False)
    grav_timeStamp = db.DateTimeField(default=datetime.datetime.utcnow)
    mag_x = db.FloatField(db.FloatField(), required=False)
    mag_y = db.FloatField(db.FloatField(), required=False)
    mag_z = db.FloatField(db.FloatField(), required=False)
    mag_timeStamp = db.DateTimeField(default=datetime.datetime.utcnow)
    orient_x = db.FloatField(db.FloatField(), required=False)
    orient_y = db.FloatField(db.FloatField(), required=False)
    orient_z = db.FloatField(db.FloatField(), required=False)
    orient_timeStamp = db.DateTimeField(default=datetime.datetime.utcnow)