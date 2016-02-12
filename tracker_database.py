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

        :param uuid: 
        Delivery status update
            :param delivered: boolean dictates the delivery status

        Location Update
            :param lat: a
            :param long:
            :param time: Given timestamp 
        
        """
        if len(args) == 1:
            delivered = args[0]
            self.curs.execute("update Packages set delivered=? where uuid=?", delivered, uuid)
        elif len(args) == 4:
            lat = args[0]
            lon = args[1]
            time = args[2]
            self.curs.execute("insert into Updates values (?,?,?,?)", (uuid, lat, lon, time))
        self.connection.commit()

    def track_new_package(self, name, uuid, lat, lon):
        """
        """
        self.curs.execute("insert into Packages values (?,?,?,?,?)", (uuid, name, lat, lon,  0))
        self.connection.commit()

    def get_package(self, uuid):
        """
        """
        self.curs.execute("select * from Packages where uuid = ?", uuid)
        return self.curs.fetchone()

    def get_package_updates(self, uuid):
        """
        """
        self.curs.execute("select * from Updates where uuid = ?", uuid)
        return self.curs.fetchone()
