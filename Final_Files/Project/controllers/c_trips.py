from schemas.trips import Trips
class TripController:
    def getSpecificTrip(id):
        return Trips.objects(id=id).first()

    def getAllTrips():
        return Trips.objects()

    def addTrips(body):
        trip_instace = [Trips(**data) for data in body]
        return Trips.objects.insert(trip_instace)

