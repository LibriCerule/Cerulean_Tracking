#!/usr/bin/python
import googlemaps
#api_key = "AIzaSyBhOIJ_Ta2QrnO2jllAy4sd5dGCzUOA4Hw"

class Directions(object):
    """

    """
    api_key = "AIzaSyBhOIJ_Ta2QrnO2jllAy4sd5dGCzUOA4Hw"
    def __init__(self):
        self.gmaps = googlemaps.Client(self.api_key)
        pass

    def getData(self, orig, dest):
        directions = self.gmaps.directions(orig, dest)

        distance = (directions[0]['legs'][0]['distance']['text']) #value is meter, text is formatted with mile
        time = (directions[0]['legs'][0]['duration']['text']) #value is seconds, text is formatted
        output = {distance, time}
        return output

