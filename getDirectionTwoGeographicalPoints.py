# import json
# import urllib3.request
# import urllib3.parse
import requests
import PolylineCode


def getDirectionTwoGeographicalPoints(origin, destination, mode):
    # Ensemble Google API query using origin and destination
    query = "http://maps.googleapis.com/maps/api/directions/json?origin=" + origin + "&destination=" + destination + "&mode=" + mode + "&language=pt-BR&sensor=false"

    webUrl = requests.get(query)

    # Execute google query
    # webUrl = urllib.request.urlopen(query)

    if webUrl.status_code == 200:
        theJSON =webUrl.json()
        # data = webUrl.read()
        # encoding = webUrl.info().get_content_charset('utf-8')
        # JSON_object = json.loads(data.decode(encoding))
        # # data1 = json.dumps(str(data))
        # # theJSON = json.loads(data1)
        # # tt = theJSON.split("\n")
        # answ = json.loads(data.decode(encoding))
        # print(data)
        # #print(theJSON)
    else:
        print("Received an error from server, cannot retrieve results" + str(webUrl.getcode()))

   # info = json.loads(query)
   # # print(info)
   #  full_distance = -1
   #  full_duration = -1
   #  paths = ""
   #
    if len(theJSON['routes']) != 0:
        #print("este")
        # Get full distance from origin to destination (in meters)
        tt =  theJSON["routes"][0]
        tt2 = tt["legs"][0]
        tt3 = tt2["distance"]
        full_distance = tt3["value"]

        # Get duration to go from origin to destination (in seconds)
        full_duration = theJSON["routes"][0]["legs"][0]["duration"]["value"]

        # Get the number of "paths blocks" (parts of the entire way)
        numSteps = len(theJSON["routes"][0]["legs"][0]["steps"])

        # Create the array "paths" to keep the path of each path block
        paths = []

        # For each path block, obtain all necessary information
        i = 0
        while i < numSteps:
            row = []
            distance = theJSON["routes"][0]["legs"][0]["steps"][i]["distance"]["value"]
            duration = theJSON["routes"][0]["legs"][0]["steps"][i]["duration"]["value"]
            start_location = str(theJSON["routes"][0]["legs"][0]["steps"][i]["start_location"]["lat"]) + "," + str(theJSON["routes"][0]["legs"][0]["steps"][i]["start_location"]["lng"])
            end_location = str(theJSON["routes"][0]["legs"][0]["steps"][i]["end_location"]["lat"]) + "," + str(theJSON["routes"][0]["legs"][0]["steps"][i]["end_location"]["lng"])
            encoded_points = theJSON["routes"][0]["legs"][0]["steps"][i]["polyline"]["points"]
            #encoded_points = PolylineCode.decode_polyline(encoded_points)
            travel_mode = theJSON["routes"][0]["legs"][0]["steps"][i]["travel_mode"]
            row = [distance, duration, start_location, end_location, encoded_points, travel_mode]
            paths.append(row)
            i += 1

    return full_distance, full_duration, paths

# getDirectionTwoGeographicalPoints("JardimdaGranja", "JardimSouto", "driving")