from schemas.gpsData import GpsData


class GpsController:

    def createGps(body):
        gps_instance = [GpsData(**data) for data in body]
        return GpsData.objects.insert(gps_instance)

    def getGPSDataForNearestNodes(node_ids):
        raw_query = {'nearest_node': {'$in': node_ids}}
        gps_data = GpsData.objects(__raw__=raw_query)
        return gps_data

    def getMaxAndMinSystemTimestampForDistinctTripIdInNodeList(nodeList):
        pipeline = [{
            '$match': {
                    'nearest_node': {'$in': nodeList}
                    }
        }, {
            '$group': {
                '_id': '$trip_id',
                'max': {'$max': '$system_timestamp'},
                'min': {'$min': '$system_timestamp'}
            }
        }, {
            '$project': {
                '_id': 0,
                'trip_id': '$_id',
                'max': 1,
                'min': 1
            }
        }
        ]

        return GpsData._get_collection().aggregate(pipeline)

    def deleteGPSData():
        return GpsData.objects.delete()
