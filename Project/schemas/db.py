from flask_mongoengine import MongoEngine
from bson.objectid import ObjectId


db = MongoEngine()
def initialize_db(app):
    db.init_app(app)