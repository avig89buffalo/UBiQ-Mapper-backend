from .db import db,ObjectId

class Way(db.Document):
    city = db.StringField( required=False)
    node_id = db.ListField(db.ObjectIdField(),required=False)