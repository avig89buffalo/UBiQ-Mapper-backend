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
