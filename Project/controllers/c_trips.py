from schemas.trips import Trips
class TripController:
    def getSpecificTrip(id):
        return Trips.objects(id=id).first()

    def getAllTrips():
        return Trips.objects()

    def createTrips(body):
        return Trips(**body).save()

