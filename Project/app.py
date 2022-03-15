import flask
from flask import Flask
import config.development
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import request, jsonify
from bson.json_util import dumps
from flask_mongoengine import MongoEngine
from config.development import Config
from schemas.db import initialize_db,db
from schemas.rawSensorData import RawSensorData
from schemas.segments import Segments
from schemas.trips import Trips
from schemas.way import Way
from schemas.node import Nodes
from controllers.c_nodes import NodeController
from controllers.c_trips import TripController
from controllers.c_segments import SegmentController
from controllers.c_way import WayController
from controllers.c_rawSensor import RawSensorDataController
from flask import Flask, request, Response
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': Config.MONGODBNAME,
    'host': Config.MONGODBHOSTNAME,
    'port':Config.MONGODBPORT
}
initialize_db(app)

@app.route('/')
def index():
    return 'Server Started'

@app.route('/initializeSchema')
def initialize():
    RawSensorData().save()
    Nodes().save()
    Segments().save()
    Trips().save()
    Way().save()
    return 'Scehema initialized'

#Nodes API's
@app.route('/node/getAll')
def getAllNodes():
    data = NodeController.getAllNodes()
    return jsonify(data),200

@app.route('/node/<id>')
def getOneNode(id: ObjectId):
    data = NodeController.getSpecificNode()
    return jsonify(data), 200

@app.route('/node', methods=["POST"])
def addNodes():
    body = request.get_json()
    data = NodeController.createNode(body)
    return jsonify(data), 201


#Trips API's
@app.route('/trip/getAll')
def getAllTrips():
    data = TripController.getAllTrips()
    return jsonify(data),200

@app.route('/trip/<id>')
def getOneTrip(id: ObjectId):
    data = TripController.getSpecificTrip()
    return jsonify(data), 200

@app.route('/trip', methods=["POST"])
def addTrips():
    body = request.get_json()
    data = TripController.createTrip(body)
    return jsonify(data), 201

#RawSensorData API's
@app.route('/way/getAll',methods=["GET"])
def getAllSensorData():
    data = RawSensorDataController.getSpecificSensorData()
    return jsonify(data),200

@app.route('/way/<id>',methods=["GET"])
def getOneSensorData(id: ObjectId):
    data = RawSensorDataController.getSpecificSensorData()
    return jsonify(data), 200

@app.route('/way', methods=["POST"])
def addSensorData():
    body = request.get_json()
    data = RawSensorDataController.createSensorData(body)
    return jsonify(data), 201

#Segments API's
@app.route('/segment/getAll',)
def getAllSegments():
    data = SegmentController.getAllSegments()
    return jsonify(data),200

@app.route('/segment/<id>')
def getOneSegment(id: ObjectId):
    data = SegmentController.getSpecificSegment()
    return jsonify(data), 200

@app.route('/segment', methods=["POST"])
def addSegment():
    body = request.get_json()
    data = SegmentController.createSegment(body)
    return jsonify(data), 201

#Way API's
@app.route('/way/getAll',methods=["GET"])
def getAllWays():
    data = WayController.getAllWays()
    return jsonify(data),200

@app.route('/way/<id>',methods=["GET"])
def getOneWay(id: ObjectId):
    data = WayController.getSpecificWay()
    return jsonify(data), 200

@app.route('/way', methods=["POST"])
def addWay():
    body = request.get_json()
    data = WayController.createWay(body)
    return jsonify(data), 201

if __name__=="__main__":
    app.run(debug=True)