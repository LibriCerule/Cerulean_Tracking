###Software Documentation:
To set up the environment, run the setup.py file
In order to start the server, run the web.py file


###Product Documentation:
The clients will then connect to the IP address and will be met with a map and a sidebar to the right with a register and login button to the top right.

####The user will have the option to:
#####Register
On successful account creation, a username and a hashed password will be paired together to create the user account.
The user will be able to login with the same credentials.

#####Login
On successful login, the user will have a list of his packages in the sidebar.
Any additional packages searched by the user will be added to his account.
Packages that are looked at will show up with markers on the map.

#####Search
Any packages that are searched for while not in a user login session will still show up on the map, but will not be stored in any account.

#####Map View
The map displays the current latitude and longitude of the package being tracked.

###Software Requirements:
####Communication Protocols and Interfaces
**Summary**: The software must communicate with the client’s service for package tracking. It must receive GPS updates which contain data on current location (longitude/latitude), elevation, time, and unique identifier of each package. It software must communicate with the client’s software endpoints using a representational state transfer (RESTful) API provided by the client. 

**Solution**: The product will use a graphical interface to display the current package display.

####Package Time Estimation in Package Information
**Summary**: The software must calculate and display an accurate estimate on the arrival time of each package. 

**Solution**: The Google Maps API gave accurate time estimation between any two given pairs of latitudes and longitudes

####Package Distance Estimation in Package Information
**Summary**: The software must display the estimated distance from the current location of the package to its destination point. 

**Solution**: The Google Maps API gave accurate distance estimation between any two given pairs of latitudes and longitudes.

####Package Delivery Status in Package Information and Package List
**Summary**: The software must indicate the status of the package among the following labels: At Facility, Departed, In Transit, Delivered, and Exception.

**Solution**: When the package is delivered, the package will no longer show up in the user’s package list.

####Checkpointing in Package Travel Map
**Summary**: The software must display each individual checkpoint on a map of the package as it travels. 

**Solution**: The latest location of the package is displayed at any arbitrary moment by storing latest GPS coordinates and updating the embedded Google Map to display it.

####Package Update
**Summary**: Information about each package can be periodically updated with an interface from an external object

**Solution**: The software will be able to update its database (sqlite3) through HTTP POST requests.
