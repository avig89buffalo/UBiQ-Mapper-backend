from schemas.rawSensorData import RawSensorData
class RawSensorDataController:
    def getSpecificSensorData(id):
        return RawSensorData.objects(id=id).first()

    def getAllSensorData():
        return RawSensorData.objects()

    def createSensorData(body):
        return RawSensorData(**body).save()
