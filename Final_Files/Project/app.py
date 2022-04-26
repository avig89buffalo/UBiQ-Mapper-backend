import flask
from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import request, jsonify
import json
from bson.json_util import dumps
from flask_mongoengine import MongoEngine
from config.development import Config
from schemas.db import initialize_db,db
from schemas.rawSensorData import RawSensorData
from schemas.segments import Segments
from schemas.trips import Trips
from schemas.way import Way
from schemas.node import Nodes
from schemas.gpsData import GpsData
from schemas.filteredPitchData import FilteredPitchData
from schemas.anchorSnapshotsData import AnchorSnapshotsData
from schemas.pitchRateFilteredData import PitchRateFilteredData
from schemas.nodeSegmentMapping import NodeSegmentMapping
from controllers.c_nodes import NodeController
from controllers.c_trips import TripController
from controllers.c_segments import SegmentController
from controllers.c_way import WayController
from controllers.c_rawSensor import RawSensorDataController
from controllers.c_gps import GpsController
from controllers.c_filteredPitch import FilteredPitchController
from controllers.c_anchorSnapshots import AnchorSnapshotsController
from controllers.c_pitchRateFiltered import PitchRateFilteredController
from controllers.c_parse_user_data import ParseUserData
from controllers.c_nodeSegmentMapping import NodeSegmentMappingConroller
from flask import Flask, request, Response
from bson.objectid import ObjectId
from frontend.controller.c_frontend import FrontendController
from frontend.validators.v_frontend import FrontendValidator
from werkzeug.exceptions import HTTPException
from controllers.c_aggregationFramework import AggregationFrameworkController
from bson import json_util

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': Config.MONGODBNAME,
    'host': Config.MONGODBHOSTNAME,
    'port':Config.MONGODBPORT
}

initialize_db(app)


@app.route('/')
def index():
    # getUserData()
    return 'Server Started'

@app.route('/initializeSchema')
def initialize():
    RawSensorData().save()
    Nodes().save()
    Segments().save()
    Trips().save()
    Way().save()
    GpsData().save()
    FilteredPitchData().save()
    AnchorSnapshotsData().save()
    PitchRateFilteredData().save()
    return 'Scehema initialized'

#Parse User data
def getUserData():
    ParseUserData.readFiles(Config.USERDATAPATH)

#Nodes API's
@app.route('/node/getAll')
def getAllNodes():
    data = NodeController.getAllNodes()
    return jsonify(data),200

@app.route('/node/<id>')
def getOneNode(id):
    data = NodeController.getSpecificNode(id)
    return jsonify(data), 200

@app.route('/node', methods=["POST"])
def addNodes():
    body = request.get_json()
    data = NodeController.createNode(body)
    return jsonify(data), 201

@app.route('/node/nearestNode', methods=["GET"])
def getNearestNode():
    body = request.get_json()
    data = NodeController.getNearestNode(body['lat_min'],body['lat_max'],body['long_min'],body['long_max'])
    return jsonify(data), 201


@app.route('/node/getMultipleNodes', methods=["GET"])
def getMultipleNodes():
    body = request.get_json()
    data = NodeController.getMultipleNodes(body['node_ids'])
    return jsonify(data), 201

@app.route('/node/updateNodeSegment', methods=["PUT"])
def updateNodeSegment():
    body = request.get_json()
    data = NodeController.updateNodeSegment(body)
    return jsonify(data), 201

@app.route('/node/userNearestNode', methods=["GET"])
def nearestNode():
    body = request.get_json()
    # print('User Nearest Node')
    # coordinate =  request.args.get('coordinate')
    data = NodeController.getUserNearestNode(body)
    return jsonify(data), 200

#Trips API's
@app.route('/trip/getAll')
def getAllTrips():
    data = TripController.getAllTrips()
    return jsonify(data),200

@app.route('/trip/<id>')
def getOneTrip(id):
    data = TripController.getSpecificTrip(id)
    return jsonify(data), 200

@app.route('/trip', methods=["POST"])
def addTrips():
    body = request.get_json()
    data = TripController.addTrips(body)
    return jsonify(data), 201

#Segments API's
@app.route('/segment/getAll',)
def getAllSegments():
    data = SegmentController.getAllSegments()
    return jsonify(data),200

@app.route('/segment/<id>')
def getOneSegment(id):
    data = SegmentController.getSpecificSegment(id)
    return jsonify(data), 200

@app.route('/segment', methods=["POST"])
def addSegment():
    body = request.get_json()
    data = SegmentController.createSegment(body)
    return jsonify(data), 201

@app.route('/segment/updateTrip', methods=["POST"])
def updateSegments():
    body = request.get_json()
    data = SegmentController.updateSegments(body)
    return jsonify(data), 201

#Way API's
@app.route('/way/getAll',methods=["GET"])
def getAllWays():
    data = WayController.getAllWays()
    return jsonify(data),200

@app.route('/way/<id>',methods=["GET"])
def getOneWay(id):
    data = WayController.getSpecificWay(id)
    return jsonify(data), 200

@app.route('/way', methods=["POST"])
def addWay():
    body = request.get_json()
    data = WayController.createWay(body)
    return jsonify(data), 201

@app.route('/cityWay',methods=["GET"])
def getCityWays():
    city =  request.args.get('city')
    data = WayController.getCityWays(city)
    return jsonify(data), 200

#GPS Data API's
@app.route('/gps', methods=["POST"])
def addGps():
    print("Got GPS Request")
    body = request.get_json()
    data = GpsController.createGps(body)
    return jsonify(data), 201

#Filtered Pitch Data API's
@app.route('/filteredPitch', methods=["POST"])
def addFilteredPitch():
    body = request.get_json()
    data = FilteredPitchController.createFilteredPitch(body)
    return jsonify(data), 201

#Anchor Snapshots Data API's
@app.route('/anchorSnapshots', methods=["POST"])
def addAnchorSnapshots():
    body = request.get_json()
    data = AnchorSnapshotsController.createAnchorSnapshots(body)
    return jsonify(data), 201

#Pitch Rate Filtered API's
@app.route('/pitchRateFiltered', methods=["POST"])
def addPitchRateFiltered():
    body = request.get_json()
    data = PitchRateFilteredController.createPitchRateFiltered(body)
    return jsonify(data), 201

#Node Segment Mapping API's
@app.route('/nodeSegmentMapping', methods=["POST"])
def addNodeSegmentMapping():
    body = request.get_json()
    data = NodeSegmentMappingConroller.createNodeSegmentMapping(body)
    return jsonify(data), 201

@app.route('/nodeSegments', methods=["get"])
def nodeSegments():
    body = request.get_json()
    data = NodeSegmentMappingConroller.getNodeSegments(body)
    return jsonify(data), 201

@app.route('/segments/getSegmentsWithTrips',methods=["GET"])
def getallsegmentsdata():
    return json_util.dumps(AggregationFrameworkController.getAllSegmentsAsList()),200
    
@app.route('/segmentElevation/createSegmentElevations',methods=["POST"])
def createSegmentElevations():
    AggregationFrameworkController.insertSegmentElevations(request.get_json()['segment'])
    return "Success",201

@app.route('/segmentElevation/getSegmentElevationsForBoundingBox',methods=["POST"])
def getSegmentElevationsForBoundingBox():
    try:
        lat1,lat2,long1,long2 = FrontendValidator.validate_bounding_box(request.get_json()['lat1'],request.get_json()['lat2'],request.get_json()['long1'],request.get_json()['long2'])
    except HTTPException as e:
        return 'Invalid Parameters',400
    return jsonify(FrontendController.processSegmentElevations(lat1,long1,lat2,long2)),200

if __name__=="__main__":
    app.run(host='0.0.0.0',port=8080)