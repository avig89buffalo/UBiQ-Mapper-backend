from .db import db,ObjectId

class NodeSegmentMapping(db.Document):
    node_id = db.FloatField(required=False)
    segment_id = db.StringField(required=False)