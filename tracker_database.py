import sqlite3
import time

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
        self.curs = self.connection.cursor()

        self.curs.execute("create table if not exists Packages (uuid varchar(60), destination varchar(255), latitude real, longitude real, delivered integer)")
        self.curs.execute("create table if not exists Updates (uuid varchar(60), latitude real, longitude real, timestamp varchar(255)")

    def package_track_update(self, uuid, delivered=None, lat=None, lon=None, ele=None, time=None):
        self.curs.execute("insert into Updates values (?,?,?,?)", (uuid, lat, lon, time))
        self.connection.commit()

    def track_new_package(self, name, uuid, lat, lon):
        self.curs.execute("insert into Packages values (?,?,?,?,?)", (uuid, name, lat, lon,  0))
        self.connection.commit()

    def get_package(self, uuid):
        pass
