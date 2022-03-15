from schemas.node import Nodes
class NodeController:
    # def updateNodes(id,lat,long):
    #     Nodes()
    def getSpecificNode(id):
        return Nodes.objects(id=id).first()

    def getAllNodes():
        return Nodes.objects()

    def createNode(body):
        return Nodes(**body).save()

