from tracker_database import TrackerDatabase 
test_uuid = "de305d54-75b4-431b-adb2-eb6b9e546014"
test_uuid2 = "de305d54-75b4-431b-adb2-eb6b9e546015"

def test_track_new_package():
    test_name = "4401 Wilson Blvd #810, Arlington, VA 22203"
    test_lat = 0
    test_lon = 0
    test_delivered = False
    test_time = "2015-12-08T08:42:33.188-25:00"

 
    testdb = TrackerDatabase("unittest.db")
    testdb.track_new_package(test_name, test_uuid, test_lat, test_lon)
    testdb.track_new_package(test_name, test_uuid2, test_lat, test_lon)

    testdb.package_track_update(test_uuid, test_lat, test_lon, test_time)
    testdb.package_track_update(test_uuid2, test_lat, test_lon, test_time)

    testdb.package_track_update(test_uuid, True)


    a = testdb.get_package(test_uuid)
    b = testdb.get_package_updates(test_uuid)
    print(a)
    #print(b)

def test_login():
    testdb = TrackerDatabase("unittest.db")
    testdb.register_user("hee", "hoo")
    if testdb.log_in("hee", "hah"):
        print("Login works!")
    else: 
        print("Login failed")
    testdb.register_package_to_user("hee", test_uuid)
    testdb.register_package_to_user("hee", test_uuid2)

    print(testdb.get_package_of_user("admin"))


def main():
   test_track_new_package()

   test_login()

if __name__ == "__main__":
    main()
