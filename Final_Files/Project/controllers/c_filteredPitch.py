from schemas.filteredPitchData import FilteredPitchData
class FilteredPitchController:
    def createFilteredPitch(body):
        filtered_pitch_instance = [FilteredPitchData(**data) for data in body]
        return FilteredPitchData.objects.insert(filtered_pitch_instance)
    
    def getFilterPitchForTripIdAndSystemTime(tripid,max_sytem_timestamp,min_sytem_timestamp):
        return FilteredPitchData.objects(trip_id=tripid,timestamp__gte=min_sytem_timestamp,timestamp__lte=max_sytem_timestamp)