from schemas.pitchRateFilteredData import PitchRateFilteredData
class PitchRateFilteredController:
    # def getSpecificWay():
    #     return Way.objects(id=id).first()

    # def getAllWays():
    #     return Way.objects()

    def createPitchRateFiltered(body):
        pitch_filtered_instance = [PitchRateFilteredData(**data) for data in body]
        return PitchRateFilteredData.objects.insert(pitch_filtered_instance)
    
    def getPitchRateFilteredForTripIdAndSystemTime(tripid,max_sytem_timestamp,min_sytem_timestamp):
        return list(PitchRateFilteredData.objects(trip_id=tripid,timestamp__gte=min_sytem_timestamp,timestamp__lte=max_sytem_timestamp).as_pymongo())