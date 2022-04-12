from schemas.anchorSnapshotsData import AnchorSnapshotsData
class AnchorSnapshotsController:
    # def getSpecificWay():
    #     return Way.objects(id=id).first()

    # def getAllWays():
    #     return Way.objects()

    def createAnchorSnapshots(body):
        anchor_snapshots_instance = [AnchorSnapshotsData(**data) for data in body]
        return AnchorSnapshotsData.objects.insert(anchor_snapshots_instance)