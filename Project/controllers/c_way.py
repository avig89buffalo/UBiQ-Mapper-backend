from schemas.way import Way
class WayController:
    def getSpecificWay():
        return Way.objects(id=id).first()

    def getAllWays():
        return Way.objects()

    def createWay(body):
        return Way(**body).save()
