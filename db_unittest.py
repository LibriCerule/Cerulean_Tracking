from tracker_database import TrackerDatabase 

def main():
    testdb = TrackerDatabase("unittest.db")

    test_uuid = "de305d54-75b4-431b-adb2-eb6b9e546014"
    test_name = "4401 Wilson Blvd #810, Arlington, VA 22203"
    test_lat = 0
    test_lon = 0
    test_delivered = False
    test_time = "2015-12-08T08:42:33.188-25:00"

    testdb.track_new_package(test_name, test_uuid, test_lat, test_lon)
#    testdb.package_track_update(test_uuid, test_lat + 1, test_lon + 1, test_time)
    testdb.package_track_update(test_uuid, True)

    a = testdb.get_package(test_uuid)
    b = testdb.get_package(test_uuid)
    print(b)


if __name__ == "__main__":
    main()
