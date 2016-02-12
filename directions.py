#!/usr/bin/python
import googlemaps

class Directions(object):
    """

    """
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.api_key = f.read()
            f.close()
        self.gmaps = googlemaps.Client(self.api_key)
        pass

    def getData(self, orig, dest):
        directions = self.gmaps.directions(orig, dest)

        distance = (directions[0]['legs'][0]['distance']['text']) #value is meter, text is formatted with mile
        time = (directions[0]['legs'][0]['duration']['text']) #value is seconds, text is formatted
        output = {distance, time}
        return output

