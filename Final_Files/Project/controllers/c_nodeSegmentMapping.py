from schemas.nodeSegmentMapping import NodeSegmentMapping
class NodeSegmentMappingConroller:

    def createNodeSegmentMapping(body):
        mapping_instance = [NodeSegmentMapping(**data) for data in body]
        return NodeSegmentMapping.objects.insert(mapping_instance)

    def getNodeSegments(body):
        raw_query = {'node_id': {'$in': body['node_ids'] }}
        segments = NodeSegmentMapping.objects(__raw__=raw_query)
        return list(set([segment['segment_id'] for segment in segments]))