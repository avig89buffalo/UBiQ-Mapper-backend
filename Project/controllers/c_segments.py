from schemas.segments import Segments
class SegmentController:
    def getSpecificSegment(id):
        return Segments.objects(id=id).first()

    def getAllSegments():
        return Segments.objects()

    def createSegment(body):
        return Segments(**body).save()
