#!/usr/bin/python
import googlemaps

class Directions(object):
    """

    """
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.api_key = f.read().strip()
            f.close()
        self.gmaps = googlemaps.Client(self.api_key)
        pass

    def getData(self, orig, dest):
        distanceData = self.gmaps.distance_matrix(orig, dest)

        time = (distanceData['rows'][0]['elements'][0]['duration']['text'])
        distance = (distanceData['rows'][0]['elements'][0]['distance']['text'])

        output = {distance, time}

        return output
