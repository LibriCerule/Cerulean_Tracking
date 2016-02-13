"""
    tracker_database.py
    ~~~~~~~~~~~~~~~~~~~
    With a "real world" application, we would sanitize all inputs and require 
    authentication to access any of these databases.

    Class to control the SQLite Database that stores packages and their updates.

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
        print(trackerdb.get_package("de305d54-75b4-431b-adb2-eb6b9e546014"))

"""

import sqlite3
import hashlib

class TrackerDatabase(object):
    def __init__(self, directory):
        """ Creates the databases if it doesn't already exist and establishes 
        connection.

        :param directory: Directory to store the sqlite database
        """

        self.connection = sqlite3.connect(directory)
        self.cursor = self.connection.cursor()

        self.cursor.execute("create table if not exists Users (username varchar(255), password_hash varchar(255), registered_packages varchar(255), num_packages int, UNIQUE(username))")
        self.cursor.execute("create table if not exists Packages (uuid varchar(60), name varchar(255), latitude real, longitude real, delivered int, UNIQUE(uuid))")
        self.cursor.execute("create table if not exists Updates (uuid varchar(60), latitude real, longitude real, timestamp varchar(255))")

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
                self.cursor.execute("delete from Updates where uuid = ?", (uuid,))
            elif str(delivered) == "False":
                delivered = 0
            else:
                raise ValueError("Delivered must be True or False")

            self.cursor.execute("update Packages set delivered=? where uuid=?", (delivered, uuid))

        elif len(args) == 3:
            lat = args[0]
            lon = args[1]
            time = args[2]
            self.cursor.execute("insert into Updates values (?,?,?,?)", (uuid, lat, lon, time))

        self.connection.commit()

    def track_new_package(self, name, uuid, lat, lon):
        """ Adds a new package to the database 

        :param name: Arbitrary name for the package
        :param uuid: Package uuid
        :param lat: Latitude of the package
        :param lon: Longitude of the package
        """


        self.cursor.execute("insert or ignore into Packages values (?,?,?,?,?)", (uuid, name, lat, lon,  0))
        self.connection.commit()

    def get_package(self, uuid):
        """ 
        :return: Tuple in the format of (uuid, name, lat, lon, delivered)
        """

        self.cursor.execute("select * from Packages where uuid = ?", (uuid,))
        return self.cursor.fetchone()

    def get_package_updates(self, uuid):
        """

        :param uuid: Package uuid

        :return: 
        """

        self.cursor.execute("select * from Updates where uuid = ?", (uuid,))
        return self.cursor.fetchall()

    def register_user(self, username, password_hash):
        """
        """
        self.cursor.execute("insert or ignore into Users values (?,?,?,?)", (username, password_hash, " ", 0))
        self.connection.commit()

    def log_in(self, username, password_hash):
        self.cursor.execute("select * from Users where username=? and password_hash=?", (username,password_hash))
        return len(self.cursor.fetchall()) == 1

    def register_package_to_user(self, username, uuid):
        self.cursor.execute("select ROWID from Packages where uuid=?", (uuid,))
        new_row_id = int(self.cursor.fetchone()[0])

        # SQLite doesn't have real lists, so we're using makeshift lists
        self.cursor.execute("select registered_packages, num_packages from Users where username=?", (username,))
        query = self.cursor.fetchone()
        registered_packages = query[0]
        num_packages = int(query[1])

        if registered_packages == " ":  # User has no registered packages
            registered_packages = new_row_id
            num_packages += 1
        else:
            # FIXME: May want to throw an exception if it tries to add a duplicate package
            if not str(new_row_id) in registered_packages.split(","):
                registered_packages += "," + str(new_row_id)
                num_packages += 1

        self.cursor.execute("update Users set num_packages=?, registered_packages=? where username=?", (num_packages, registered_packages, username))
        self.connection.commit()
