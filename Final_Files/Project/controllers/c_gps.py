from schemas.gpsData import GpsData
class GpsController:

    def createGps(body):
        gps_instance = [GpsData(**data) for data in body]
        return GpsData.objects.insert(gps_instance)
    
    def getGPSDataForNearestNodes(node_ids):
        raw_query = {'nearest_node': {'$in': node_ids }}
        gps_data = GpsData.objects(__raw__=raw_query)
        return gps_data
    
    def getMaxAndMinSystemTimestampForTripId(tripid):
        maxGpsObject=GpsData.objects(trip_id=tripid).order_by("-system_timestamp").limit(-1).first()
        minGpsObject=GpsData.objects(trip_id=tripid).order_by("+system_timestamp").limit(-1).first()
        return maxGpsObject.system_timestamp,minGpsObject.system_timestamp

    def deleteGPSData():
        return GpsData.objects.delete()
