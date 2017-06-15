import getDirectionTwoGeographicalPoints
import recordDistancesDirections
import importGeographicalPointsFromXLS
import databaseConnection

def roadsMappingService(pp, inputFile, city, state):
    # Connect with database and check if connection have been performed successfully
    con = databaseConnection.connectdb()
    cursor = con.cursor()
    if not con:
        print("Database connection ERROR!")
        exit()

    # Read from a XLS a matrix where each line is a pair of coords lat/long
    regions = importGeographicalPointsFromXLS.importGeographicalPointsFromXLS(inputFile)

    # Get the total of regions into region array
    nr = len(regions)

    # Create composed name of table
    tableName = "distances_" + city + "_" + state

    # Get last record in database
    sql = "SELECT * FROM " + tableName + " ORDER BY id DESC"
    cursor.execute(sql)
    row = cursor.fetchall()

    #row = []

    # Setup initial index of origin and destination (in regions matrix) as the last index in database
    if len(row) == 0:
        idx_origin = 0
        idx_destination = 1
    # else:
    #     idx_origin = row[1]
    #     idx_destination = row[2] + 1

    idx_origin = 0
    idx_destination = 1
    # Create pairs (origin and destination) for all the regions into regions array. For each point we have lat, long coordinates (respectively)
    cc = 1
    i = idx_origin
    while i < nr - 1:
        temp = regions[i]
        origins = str(temp[1]) + "," + str(temp[0])

        # Check if J index should start from I + 1 or using database recovered index
        if i == idx_origin:
            j = idx_destination
        else:
            j = i + 1

        while j < nr:
            temp = regions[j]
            destinations = str(temp[1]) + ',' + str(temp[0])

            '''  Get the path for driving mode forward and backward  '''

            # Mode of travel
            tempmode = "driving"

            # Get the distance for forward path
            [distance, duration, paths]= getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(origins, destinations, tempmode)
            #print(paths)

            # Record distance and path into database
            output = recordDistancesDirections.recordDistancesDirections(i, j, destinations, origins, tempmode, distance, paths, city, state, duration)
            if output == False:
                exit()


            # Get the distance for backward path
            [distance, duration, paths] = getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(destinations, origins, tempmode)
            print(paths)

            # Record distance and path into database
            output = recordDistancesDirections.recordDistancesDirections(i, j, destinations, origins, tempmode, distance, paths, city, state, duration)
            if output == False:
                exit()

            '''  Get the path for walking mode forward and backward  '''

            # Mode of travel
            tempmode = "driving"

            # Get the distance for forward path
            [distance, duration, paths] = getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(origins, destinations, tempmode)

            # Record distance and path into database
            output = recordDistancesDirections.recordDistancesDirections(i, j, destinations, origins, tempmode, distance, paths, city, state, duration)
            if output == False:
                exit()


            # Get the distance for backward path
            [distance, duration, paths] = getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(destinations, origins, tempmode)

            # Record distance and path into database
            output = recordDistancesDirections.recordDistancesDirections(i, j, destinations, origins, tempmode, distance, paths, city, state, duration)
            if output == False:
                exit()

            # Check if the script has already been executed the correct number of times. If yes stop the code. This process have been implemented because Google API has a limit of querys daily
            if cc < pp:
                cc += 1
            else:
                cc = cc
                break
            j += 1

        if cc >= pp:
            break
        i += 1

# Execute the function
roadsMappingService(50, "zonas-trafego-sjc-sp", "sjc", "sp")