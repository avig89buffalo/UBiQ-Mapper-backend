from schemas.pitchRateFilteredData import PitchRateFilteredData
class PitchRateFilteredController:
    # def getSpecificWay():
    #     return Way.objects(id=id).first()

    # def getAllWays():
    #     return Way.objects()

    def createPitchRateFiltered(body):
        pitch_filtered_instance = [PitchRateFilteredData(**data) for data in body]
        return PitchRateFilteredData.objects.insert(pitch_filtered_instance)