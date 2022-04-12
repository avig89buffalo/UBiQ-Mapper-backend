from schemas.segments import Segments
class SegmentController:
    def getSpecificSegment(id):
        return Segments.objects(id=id).first()

    def getAllSegments():
        return Segments.objects()

    def createSegment(body):
        segment_instances = [Segments(**data) for data in body]
        return Segments.objects.insert(segment_instances)
