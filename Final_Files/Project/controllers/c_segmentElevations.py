from schemas.segmentElevations import segmentElevations

class SegmentElevationsController:
    
    def getsegmentElevationsForSegmentId(segmentId):
        return segmentElevations.objects(segment_id=segmentId)
    
    def createOrUpdateSegmentElevation(segmentId,latitude,longitude,distance,elevation):
        segmentElevations.objects(segment_id=segmentId,location=[latitude,longitude]).update_one(set__distance=distance,set__elevation=elevation,upsert=True)
        
    def getAllSegmentsForBoundingBox(latitude1,latitude2,longitude1,longitude2):
        return segmentElevations.objects(location__geo_within_box=[(latitude1, longitude1), (latitude2, longitude2)]).distinct(field="segment_id")
    
    def getSegmentElevationsForGivenSegmentIds(segment_ids):
        raw_query = {'nearest_node': {'$in': segment_ids }}
        return segmentElevations.objects(__raw__=raw_query)

