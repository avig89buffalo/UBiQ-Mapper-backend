from schemas.filteredPitchData import FilteredPitchData
class FilteredPitchController:
    # def getSpecificWay():
    #     return Way.objects(id=id).first()

    # def getAllWays():
    #     return Way.objects()

    def createFilteredPitch(body):
        print("Inside Filtered Pitch")
        filtered_pitch_instance = [FilteredPitchData(**data) for data in body]
        return FilteredPitchData.objects.insert(filtered_pitch_instance)