from schemas.gpsData import GpsData
class GpsController:
    # def getSpecificWay():
    #     return Way.objects(id=id).first()

    # def getAllWays():
    #     return Way.objects()

    def createGps(body):
        print("inside GPS")
        gps_instance = [GpsData(**data) for data in body]
        print("gps Done")
        return GpsData.objects.insert(gps_instance)
    
    def getGPSDataForNearestNodes(node_ids):
        raw_query = {'nearest_node': {'$in': node_ids }}
        gps_data = GpsData.objects(__raw__=raw_query)
        return gps_data
    
    def getMaxAndMinSystemTimestampForTripId(tripid):
        max_sytem_timestamp=GpsData.objects(trip_id=tripid).order_by("-system_timestamp").limit(-1).first()
        min_sytem_timestamp=GpsData.objects(trip_id=tripid).order_by("+system_timestamp").limit(-1).first()
        return max_sytem_timestamp,min_sytem_timestamp
