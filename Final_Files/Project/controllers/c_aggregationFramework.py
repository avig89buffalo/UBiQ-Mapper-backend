from inspect import istraceback
from controllers.c_segments import SegmentController
from controllers.c_gps import GpsController
from controllers.c_nodes import NodeController
from controllers.c_anchorSnapshots import AnchorSnapshotsController
from controllers.c_pitchRateFiltered import PitchRateFilteredController
from controllers.c_filteredPitch import FilteredPitchController
from controllers.c_segmentElevations import SegmentElevationsController
import os
import csv
class AggregationFrameworkController:
    def getAllSegmentsAsList():
        segments = SegmentController.getSegmentsWithTripIds()
        global anchorSnapshotsDict
        global pitchRateFilteredDict
        global filteredPitchDict
        for segment in segments:
            segment_dict={}
            segment_dict['segment_id']=str(segment.id)
            request_list = list(set((map(int,segment.node_ids))))
            gps_data=GpsController.getGPSDataForNearestNodes(request_list)
            anchorSnapshotsList=[]
            pitchRateFilteredList=[]
            filteredPitchList=[]
            gps_list=[]
            results=GpsController.getMaxAndMinSystemTimestampForDistinctTripIdInNodeList(request_list)
            for result in results:
                anchorSnapshotsList.extend(AnchorSnapshotsController.getAnchorSnapshotsForTripIdAndSystemTime(result['trip_id'],result['max'],result['min']))
                pitchRateFilteredList.extend(PitchRateFilteredController.getPitchRateFilteredForTripIdAndSystemTime(result['trip_id'],result['max'],result['min']))
                filteredPitchList.extend(FilteredPitchController.getFilterPitchForTripIdAndSystemTime(result['trip_id'],result['max'],result['min']))
            for gps in gps_data:
                nearest_node=NodeController.getSpecificNode(gps.nearest_node)
                gps_list.append(AggregationFrameworkController.convertGpsToDict(gps,nearest_node))
            AggregationFrameworkController.writeCSVFile(str(segment.id),"anchor_snapshots",anchorSnapshotsList)
            AggregationFrameworkController.writeCSVFile(str(segment.id),"pitch_rate_filtered",pitchRateFilteredList)
            AggregationFrameworkController.writeCSVFile(str(segment.id),"filtered_pitch",filteredPitchList)
            AggregationFrameworkController.writeCSVFile(str(segment.id),"gps",gps_list)
            AggregationFrameworkController.writeCSVFile(str(segment.id),"nodes",AggregationFrameworkController.convertNodesToList(NodeController.getMultipleNodes(request_list))) 
        return 'Files created'
    
    
    def writeCSVFile(segmentid,type,data):
        if data: 
            if isinstance(data,list):
                keys=data[0].keys()
            elif isinstance(data,dict):
                keys=data.keys()
            filename='/output_files/'+segmentid +'/'+type+'.csv'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            file = open(filename, "w",newline='', encoding='utf-8')
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
            file.close()


    def convertObjectsintoListofDict(objects):
        objectList=[]
        for object in objects:
            objectdict={'timestamp':object.timestamp,'value':object.value}
            objectList.append(objectdict)
        return objectList


    @staticmethod
    def convertNodesToList(nodes):
        nodesList=[]
        for node in nodes:
            nodeDict={}
            nodeDict['node_id']=node.node_id
            nodeDict['latitude']=node.location['coordinates'][0]
            nodeDict['longtitude']=node.location['coordinates'][1]
            nodesList.append(nodeDict)
        return nodesList   
    
    @staticmethod
    def convertGpsToDict(gps,nearest_node):
        gps_dict={}
        gps_dict['trip_id']=gps.trip_id
        gps_dict['timestamp']=gps.timestamp
        gps_dict['system_timestamp']=gps.system_timestamp
        gps_dict['latitude']=gps.latitude
        gps_dict['longitude']=gps.longitude
        gps_dict['map_matched_latitude']=gps.map_matched_latitude
        gps_dict['map_matched_longitude']=gps.map_matched_longitude
        gps_dict['velocity']=gps.velocity
        gps_dict['acc']=gps.acc
        gps_dict['bearing']=gps.bearing
        gps_dict['bad_data']=gps.bad_data
        gps_dict['nearest_node_id']=nearest_node.node_id,
        gps_dict['nearest_node_latitude']=nearest_node.location['coordinates'][0]
        gps_dict['nearest_node_latitude']=nearest_node.location['coordinates'][1]
        gps_dict['city']=gps.city
        return gps_dict
    
    def insertSegmentElevations(data):
        for node in data["nodes"]:
            SegmentElevationsController.createOrUpdateSegmentElevation(data["segment_id"],node["latitude"],node["longitude"],node["distance"],node["elevation"])
            
        