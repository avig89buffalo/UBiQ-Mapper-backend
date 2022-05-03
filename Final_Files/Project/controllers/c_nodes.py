from schemas.node import Nodes
class NodeController:
    # def updateNodes(id,lat,long):
    #     Nodes()
    def getSpecificNode(id):
        return Nodes.objects(node_id=id).first()

    def getAllNodes():
        return Nodes.objects()

    def createNode(body):
        node_instances = [Nodes(**data) for data in body]
        return Nodes.objects.insert(node_instances)
        
    def deleteNodes():
        return Nodes.objects.delete()

    def getNearestNode(lat_min,lat_max,long_min,long_max):
        raw_query = {'latitude': {'$gte': lat_min, '$lt': lat_max}, 
                    'longitude': {'$gte': long_min, '$lt': long_max}}
        nodes = Nodes.objects(__raw__=raw_query)
        return nodes

    def getMultipleNodes(ids):
        raw_query = {'node_id': {'$in': ids }}
        nodes = Nodes.objects(__raw__=raw_query)
        return nodes
        
    def updateNodeSegment(body):
        node_ids = [x['node_id'] for x in body]
        segment_ids = [x['segment_id'] for x in body]
        nodes = []
        for i in range(len(segment_ids)):
            nodes.append(Nodes.objects(node_id=node_ids[i]).update(segment_id = segment_ids[i]))
        return nodes
    
    def getUserNearestNode(body):
        coordinate = body['coordinate']
        # print('Inside User Nearest Node',coordinate)
        raw_query ={"location":{
                                "$nearSphere": {
                                     "$geometry": {
                                        "type": "Point",
                                        "coordinates": coordinate},
                                     "$minDistance": 1}}}
        node = Nodes.objects(__raw__=raw_query)
        return node[0]

    def updateIntersectingNodes(body):
        node_ids = body['node_ids']
        print('Inside updateIntersectingNodes ',node_ids)
        node_ids = {'node_id': {'$in': node_ids }}
        nodes = Nodes.objects(__raw__=node_ids).update(intersecting_node = True)
        return nodes
    
    def getIntersectingNodes(ids):
        raw_query = {'node_id': {'$in': ids },
                        'intersecting_node': True}
        nodes = Nodes.objects(__raw__=raw_query)
        return nodes