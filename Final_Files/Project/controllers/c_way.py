from schemas.way import Way
class WayController:
    def getSpecificWay():
        return Way.objects(id=id).first()

    def getAllWays():
        return Way.objects()

    def createWay(body):
        way_instance = [Way(**data) for data in body]
        return Way.objects.insert(way_instance)

    def getCityWays(city):
        return Way.objects(city=city).only('node_ids')

    def deleteWays():
        return WayController.objects.delete()
