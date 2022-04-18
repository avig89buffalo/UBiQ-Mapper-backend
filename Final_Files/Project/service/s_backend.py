from controllers.c_segments import SegmentController
from controllers.c_gps import GpsController
from controllers.c_nodes import NodeController
from controllers.c_anchorSnapshots import AnchorSnapshotsController
from controllers.c_pitchRateFiltered import PitchRateFilteredController
from controllers.c_filteredPitch import FilteredPitchController
from controllers.c_segmentElevations import SegmentElevationsController

class BackendService:
    def getAllSegmentsAsList():
        segments = SegmentController.getAllSegmentswithTripIds()
        segment_list=[]
        for segment in segments:
            segment_dict={}
            segment_dict['id']=segments.id
            gps_data=GpsController.getGPSDataForNearestNodes(segment.node_ids)
            anchor_snapshots_set=set()
            pitch_rate_filtered_set=set()
            filtered_pitch_set=set()
            for gps in gps_data:
                max_sytem_timestamp,min_sytem_timestamp=GpsController.getMaxAndMinSystemTimestampForTripId(gps.trip_id)
                gps.nearest_node=NodeController.getSpecificNode(gps.nearestnode)
                anchor_snapshots_set.add(AnchorSnapshotsController.getAnchorSnapshotsForTripIdAndSystemTime(gps.trip_id,max_sytem_timestamp,min_sytem_timestamp))
                pitch_rate_filtered_set.add(PitchRateFilteredController.getPitchRateFilteredForTripIdAndSystemTime(gps.trip_id,max_sytem_timestamp,min_sytem_timestamp))
                filtered_pitch_set.add(FilteredPitchController.getFilterPitchForTripIdAndSystemTime(gps.trip_id,max_sytem_timestamp,min_sytem_timestamp))
                segment_dict['anchor_snapshots']=  list(anchor_snapshots_set)
                segment_dict['pitch_rate_filtered']=list(pitch_rate_filtered_set)
                segment_dict['filtered_pitch']=list(filtered_pitch_set)
                segment_dict['gps']=gps_data
                segment_dict['nodes']=NodeController.getMultipleNodes(segment.node_ids)
                segment_list.append(segment_dict)
                segment_dict['map_matched_coordinates'] ={"latitude":gps.map_matched_latitude,"longitude":gps.map_matched_longitude}
        segments_json={'segments':segment_list}
        return segments_json
    
    def insertSegmentElevations(data):
        for node in data["nodes"]:
            SegmentElevationsController.createOrUpdateSegmentElevation(data["segment_id"],node["latitude"],node["longitude"],node["distance"],node["elevation"])
            
        