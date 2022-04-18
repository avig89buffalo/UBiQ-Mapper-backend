from schemas.anchorSnapshotsData import AnchorSnapshotsData
class AnchorSnapshotsController:
    # def getSpecificWay():
    #     return Way.objects(id=id).first()

    # def getAllWays():
    #     return Way.objects()

    def createAnchorSnapshots(body):
        anchor_snapshots_instance = [AnchorSnapshotsData(**data) for data in body]
        return AnchorSnapshotsData.objects.insert(anchor_snapshots_instance)
    
    def getAnchorSnapshotsForTripIdAndSystemTime(tripid,max_sytem_timestamp,min_sytem_timestamp):
        return AnchorSnapshotsData.objects(trip_id=tripid,timestamp__gte=min_sytem_timestamp,timestamp__lte=max_sytem_timestamp)