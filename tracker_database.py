import sqlite3
class TrackerDatabase(object):
    """
        DB Scheme is as follows:
          Packages Table:
          _____________________________________________________________________
          | UUID | Destination | Latitude | Longitude | Timestamp | Delivered |
          ---------------------------------------------------------------------
          UUID - Unique tracking ID per-package
          Destination - Address of the destination
          Latitude - The latitude of the destination
          Longitude - The longitude of the destination
          Timestamp - Starting time of the package
          Delivered - Integer value of 1 if the package has been delivered already, 
                      otherwise 0
        

    """

    def __init__(self):
        """
            Performs first-time setup of the database if it doesn't already exist
        """

        self.connection = sqlite3.connect("package.db")
        self.curs = connection.cursor()

        self.curs.execute("create table if not exists Packages (uuid varchar(60), destination varchar(255), latitude real, longitude real, timestamp integer, delivered integer)")
        self.curs.execute("create table if not exists Updates (uuid varchar(60), latitude, longitude, timestamp)")

    def package_track_update(uuid, delivered=None, lat=None, lon=None, ele=None, time=None):
        pass

    def track_new_package(name, uuid, lat, lon):
        pass

    def get_package(uuid):
        pass


