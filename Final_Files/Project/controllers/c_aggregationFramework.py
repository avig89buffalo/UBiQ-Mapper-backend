from controllers.c_segments import SegmentController
from controllers.c_gps import GpsController
from controllers.c_nodes import NodeController
from controllers.c_anchorSnapshots import AnchorSnapshotsController
from controllers.c_pitchRateFiltered import PitchRateFilteredController
from controllers.c_filteredPitch import FilteredPitchController
from controllers.c_segmentElevations import SegmentElevationsController



class AggregationFrameworkController:
    def getAllSegmentsAsList():
        segments = SegmentController.getAllSegmentswithTripIds()
        segment_list=[]
        global anchorSnapshotsDict
        global pitchRateFilteredDict
        global filteredPitchDict
        for segment in segments:
            segment_dict={}
            segment_dict['segment_id']=segments.id
            gps_data=GpsController.getGPSDataForNearestNodes(segment.node_ids)
            anchorSnapshotsDict={}
            pitchRateFilteredDict={}
            filteredPitchDict={}
            gps_list=[]
            for gps in gps_data:
                max_sytem_timestamp,min_sytem_timestamp=GpsController.getMaxAndMinSystemTimestampForTripId(gps.trip_id)
                nearest_node=NodeController.getSpecificNode(gps.nearestnode)
                AggregationFrameworkController.convertAnchorSnapshotsObjectsToDict(AnchorSnapshotsController.getAnchorSnapshotsForTripIdAndSystemTime(gps.trip_id,max_sytem_timestamp,min_sytem_timestamp))
                AggregationFrameworkController.convertPitchRateFilteredObjectsToDict(PitchRateFilteredController.getPitchRateFilteredForTripIdAndSystemTime(gps.trip_id,max_sytem_timestamp,min_sytem_timestamp))
                AggregationFrameworkController.convertFilteredPitchObjectsToDict(FilteredPitchController.getFilterPitchForTripIdAndSystemTime(gps.trip_id,max_sytem_timestamp,min_sytem_timestamp))
                gps_list.append(AggregationFrameworkController.convertGpsToDict(gps,nearest_node))
            segment_dict['anchor_snapshots']=list(anchorSnapshotsDict.values())
            segment_dict['pitch_rate_filtered']=list(pitchRateFilteredDict.values())
            segment_dict['filtered_pitch']=list(filteredPitchDict.values())
            segment_dict['gps']=gps_list
            segment_dict['nodes']=AggregationFrameworkController.convertNodesToList(NodeController.getMultipleNodes(segment.node_ids))
            segment_list.append(segment_dict)
        
        segments_json={'segments':segment_list}
        return segments_json
    
    @staticmethod
    def convertNodesToList(nodes):
        nodesList=[]
        for node in nodes:
            nodeDict={}
            nodeDict['node_id']=node.node_id
            nodeDict['latitude']=node.location[0]
            nodeDict['longtitude']=node.location[1]
            nodesList.append(nodeDict)
        return nodesList   
            

            
    
    @staticmethod
    def convertAnchorSnapshotsObjectsToDict(objects):  
        for object in objects:
            anchorSnapshotsDict[object.trip_id+object.timestamp]={'timestamp':object.timestamp,'value':object.value}

    @staticmethod
    def convertPitchRateFilteredObjectsToDict(objects):  
        for object in objects:
            pitchRateFilteredDict[object.trip_id+object.timestamp]={'timestamp':object.timestamp,'value':object.value}
    
    @staticmethod
    def convertFilteredPitchObjectsToDict(objects):  
        for object in objects:
            filteredPitchDict[object.trip_id+object.timestamp]={'timestamp':object.timestamp,'value':object.value}
        
        
    
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
        gps_dict['nearest_node']={'node_id':nearest_node.node_id,'latitude':nearest_node.location[0],'longitude':nearest_node.location[1]}
        gps_dict['city']=gps.city
        return gps_dict
    
    def insertSegmentElevations(data):
        for node in data["nodes"]:
            SegmentElevationsController.createOrUpdateSegmentElevation(data["segment_id"],node["latitude"],node["longitude"],node["distance"],node["elevation"])
            
        