from schemas.segments import Segments
from bson.objectid import ObjectId
class SegmentController:
    def getSpecificSegment(id):
        return Segments.objects(id=id).first()

    def getAllSegments():
        return Segments.objects()

    def createSegment(body):
        segment_instances = [Segments(**data) for data in body]
        print(segment_instances)
        return Segments.objects.insert(segment_instances)

    def deleteSegments():
        return Segments.objects.delete()

    def updateSegments(body):
        objid = []
        results = []
        for i in body['segments']:
            board = Segments.objects(id=ObjectId(i)).get()
            board.trip_ids.append(body['trip_id'])
            results.append(board.save())
        return results 

    def getSegmentsWithTripIds():
        return Segments.objects(trip_ids__0__exists=True)