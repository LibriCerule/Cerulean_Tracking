"""
    tracker_database.py
    ~~~~~~~~~~~~~~~~~~~
    Class to control the SQLite Database that stores packages and their updates.
    With a "real world" application, we would sanitize all inputs and require 
    authentication to access this database.

    The database scheme is as follows:

        Packages Table:
          ______________________________________________________________
          | UUID | Name | Latitude | Longitude | Timestamp | Delivered |
          --------------------------------------------------------------

          UUID - Unique tracking ID per-package
          Name - Arbitrary name for the package
          Latitude - The latitude of the destination
          Longitude - The longitude of the destination
          Timestamp - Starting time of the package
          Delivered - Integer value of 1 if the package has been delivered already, 
                      otherwise 0
        
        Updates Table:
          ___________________________________________
          | UUID | Latitude | Longitude | Timestamp |
          -------------------------------------------

          UUID - Unique tracking ID per-package
          Name - Arbitrary name for the package
          Latitude - The latitude of the package
          Longitude - The longitude of the package
          Timestamp - Starting time of the package


    Example usage of the class:

        trackerdb = TrackerDatabase("/path/to/directory")

        # Create new package
        trackerdb.track_new_package("Arizona Iced Tea", "de305d54-75b4-431b-adb2-eb6b9e546014", 38.880513, -77.113585)

        # 
        a

"""

import sqlite3
import time

class TrackerDatabase(object):
    def __init__(self, directory):
        """ Creates the databases if it doesn't already exist and establishes 
        connection.

        :param directory: Directory to store the sqlite database
        """

        self.connection = sqlite3.connect(directory)
        self.curs = self.connection.cursor()

        self.curs.execute("create table if not exists Packages (uuid varchar(60), destination varchar(255), latitude real, longitude real, delivered integer)")
        self.curs.execute("create table if not exists Updates (uuid varchar(60), latitude real, longitude real, timestamp varchar(255))")

    def package_track_update(self, uuid, *args):
        """ Creates a new entry in the package tracker updates table. There is 
        no true function overloading in python, so this is our workaround.

        There are two packge track modes:
            Delivery status update
            Location update

        Delivery status update
            :param uuid: Package uuid
            :param delivered: boolean dictates the delivery status

        Location Update
            :param uuid: Package uuid
            :param lat: Latitude of the package
            :param lon: Longitude of the package
            :param time: Timestamp from the event
        """

        if len(args) == 1:
            delivered = args[0]
            if str(delivered) == "True":
                delivered = 1
            elif str(delivered) == "False":
                delivered = 0
            else:
                raise ValueError("Delivered must be True or False")

            self.curs.execute("update Packages set delivered=? where uuid=?", (delivered, uuid))

        elif len(args) == 3:
            lat = args[0]
            lon = args[1]
            time = args[2]
            self.curs.execute("insert into Updates values (?,?,?,?)", (uuid, lat, lon, time))

        self.connection.commit()

    def track_new_package(self, name, uuid, lat, lon):
        """ Adds a new package to the database 

        :param name: Arbitrary name for the package
        :param uuid: Package uuid
        :param lat: Latitude of the package
        :param lon: Longitude of the package
        """


        self.curs.execute("insert into Packages values (?,?,?,?,?)", (uuid, name, lat, lon,  0))
        self.connection.commit()

    def get_package(self, uuid):
        """ 
        :return: Tuple in the format of (uuid, name, lat, lon, delivered)
        """

        self.curs.execute("select * from Packages where uuid = ?", (uuid,))
        return self.curs.fetchone()

    def get_package_updates(self, uuid):
        """

        :param uuid: Package uuid

        :return: 
        """

        self.curs.execute("select * from Updates where uuid = ?", (uuid,))
        return self.curs.fetchall()
