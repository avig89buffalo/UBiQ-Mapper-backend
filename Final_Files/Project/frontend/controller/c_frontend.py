import json
from controllers.c_segmentElevations import SegmentElevationsController

class FrontendController:
    def processSegmentElevations(lat1,long1,lat2,long2):
        segment_ids_within_bounding_box=SegmentElevationsController.getAllSegmentsForBoundingBox(lat1,long1,lat2,long2)
        segment_elevation_list=[]
        for segment_id in segment_ids_within_bounding_box:
            limit=60
            segmentElevations=SegmentElevationsController.getsegmentElevationsForSegmentId(segment_id)
            segment_list=[]
            for segmentElevation in segmentElevations:
                if(int(segmentElevation.distance)==limit):
                    segment_list.append([segmentElevation.location[0],segmentElevation.location[1],segmentElevation.elevation,segmentElevation.distance])
                    limit+=60
                    segment_elevation_list.append(segment_list)
                    segment_list=[]
                else:
                    segment_list.append([segmentElevation.location[0],segmentElevation.location[1],segmentElevation.elevation,segmentElevation.distance])
            segment_elevation_list.append(segment_list)
        return segment_elevation_list
                
                                       
            
    
    
    

