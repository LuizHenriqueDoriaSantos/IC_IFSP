import PolylineCode
import databaseConnection

def generateKMLFile(numRecords, city, state):
    # Connect with database and check if connection have been performed successfully
    con = databaseConnection.connectdb()
    cursor = con.cursor()
    if not con:
        print("Database connection ERROR!")
        exit()

    # Create composed name of table
    tableName = "distances_" + city + "_" + state

    # Create composed name of table where intermediate paths are
    intermediateTableName = "intermiate_distances_" + city + "_" + state

    # Create the name of the foreing key into intermediate table
    idname = "id_distances_" + city + "_" + state

    # Get all the records in database that have not been processed yet
    sql = "SELECT * FROM " + tableName + " WHERE processed = 0 ORDER BY id"
    result = cursor.execute(sql)

    i = 0

    # Create an object of class Polyline to decode path
    # polyline = Polyline

    # Create a KML file for each not processed record
    row = cursor.fetchall()
    while i < len(row):
        id_full_path = row[i][0]
        print(i)

        # Invert coordinates (lat,long to long,lat) for origin and destination. Also removes "(" and ")" from string
        origin = row[i][3]
        origin = origin.strip("(")
        origin = origin.strip(")")
        tmp = origin.split(",")
        origin = tmp[0] + ', ' + tmp[1]
        nameorigin = origin

        destination = row[i][4]
        destination = destination.strip("(")
        destination = destination.strip(")")
        tmp = destination.split(",")
        destination = tmp[0] + ', ' + tmp[1]
        namedestination = destination

        mode = row[i][6].strip()

        path_str = ""

        # Get the encoded path and transform it into a string
        encoded_points = row[i][7].split(" ")
        decoded_points = []
        numPaths = len(encoded_points)
        j = 0
        while j < numPaths:
            tmp = encoded_points[j]
            decoded_points = PolylineCode.decode_polyline(tmp)
            # decoded_points = polylineCode.PolylineClass.Par(polylineCode.PolylineClass.Decode(tmp))
            k = 0
            while k < len(decoded_points):
                tmp = decoded_points[k]
                path_str = path_str + str(tmp[1]) + "," + str(tmp[0]) + ",0.0 "
                k += 1
            j += 1

        path_str = path_str.strip()

        # Create coordinates for origin and destination
        tmp = origin.split(", ")
        path_origin = str(tmp[1]) + ',' + str(tmp[0]) + ',0.00'
        tmp = destination.split(", ")
        path_destination = str(tmp[1]) + ',' + str(tmp[0]) + ',0.00'

        file_name = "C:/Users/Luiz/Google Drive/0 - Projeto Iniciação Científica/IniciacaoCientifica/IniciacaoCientifica/new_KML_file/" + mode + "_from_" + nameorigin + "_to_" + namedestination + "_part_00.kml"
        fp = open(file_name, 'w')
        # print(fp, xmlstring)

        # Assembly XML string
        fp.write("<?xml version='1.0' encoding='UTF-8'?>")
        fp.write("<kml xmlns='http://www.opengis.net/kml/2.2'>")
        fp.write("\t<Document>\n")
        fp.write("\t\t<name>Directions from " + origin + " to " + destination + "</name>\n")
        fp.write("\t\t\t<Placemark>\n")
        fp.write("\t\t\t\t<styleUrl>#line-1267FF-5</styleUrl>\n")
        fp.write("\t\t\t\t<name>Directions from " + origin + " to " + destination + "</name>\n")
        fp.write("\t\t\t\t<ExtendedData>\n")
        fp.write("\t\t\t\t</ExtendedData>\n")
        fp.write("\t\t\t\t<LineString>\n")
        fp.write("\t\t\t\t<tessellate>1</tessellate>\n")
        fp.write("\t\t\t\t\t<coordinates>" + path_str + "</coordinates>\n")
        fp.write("\t\t\t\t</LineString>\n")
        fp.write("\t\t\t</Placemark>\n")
        fp.write("\t\t\t<Placemark>\n")
        fp.write("\t\t\t<styleUrl>#icon-503-DB4436</styleUrl>\n")
        fp.write("\t\t\t\t<name>" + origin + "</name>\n")
        fp.write("\t\t\t\t<ExtendedData>\n")
        fp.write("\t\t\t\t</ExtendedData>\n")
        fp.write("\t\t\t\t<description><![CDATA[Origin]]></description>\n")
        fp.write("\t\t\t\t<Point>\n")
        fp.write("\t\t\t\t\t<coordinates>" + path_origin + "</coordinates>\n")
        fp.write("\t\t\t\t</Point>\n")
        fp.write("\t\t\t</Placemark>\n")
        fp.write("\t\t\t<Placemark>\n")
        fp.write("\t\t\t\t<styleUrl>#icon-503-DB4436</styleUrl>\n")
        fp.write("\t\t\t\t<name>" + destination + "</name>\n")
        fp.write("\t\t\t\t<ExtendedData>\n")
        fp.write("\t\t\t\t</ExtendedData>\n")
        fp.write("\t\t\t\t<description><![CDATA[Destination]]></description>\n")
        fp.write("\t\t\t\t<Point>\n")
        fp.write("\t\t\t\t\t<coordinates>" + path_destination + "</coordinates>\n")
        fp.write("\t\t\t\t</Point>\n")
        fp.write("\t\t\t</Placemark>\n")
        fp.write("\t\t\t<Style id='icon-503-DB4436'>\n")
        fp.write("\t\t\t\t<IconStyle>\n")
        fp.write("\t\t\t\t\t<color>ff3644DB</color>\n")
        fp.write("\t\t\t\t\t<scale>1.1</scale>\n")
        fp.write("\t\t\t\t\t<Icon>\n")
        fp.write("\t\t\t\t\t\t<href>http://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>\n")
        fp.write("\t\t\t\t\t</Icon>\n")
        fp.write("\t\t\t\t</IconStyle>\n")
        fp.write("\t\t\t</Style>\n")
        fp.write("\t\t\t<Style id='line-1267FF-5'>\n")
        fp.write("\t\t\t\t<LineStyle>\n")
        fp.write("\t\t\t\t\t<color>ffFF6712</color>\n")
        fp.write("\t\t\t\t\t<width>5</width>\n")
        fp.write("\t\t\t\t</LineStyle>\n")
        fp.write("\t\t\t</Style>\n")
        fp.write("\t</Document>\n")
        fp.write("</kml>\n")

        fp.close()

        # Update database record status to point out that it have already been processed
        sql2 = "UPDATE " + tableName + " SET processed = '1' WHERE id = '" + str(id_full_path) + "'"
        result2 = cursor.execute(sql2)
        i += 1

        # Get intermediate paths from an specific id
        sql2 = "SELECT * FROM " + intermediateTableName + " WHERE '" + str(idname) + "' = '" + str(id_full_path) + "' ORDER BY id DESC"
        resultIntermediate = cursor.execute(sql2)
        part = 1

        # For each intermediate part of path, construct a KML file
        rowIntermediate = cursor.fetchall()

        while rowIntermediate:

            # Get data from database for intermediate paths
            distance = rowIntermediate[7]

            duration = rowIntermediate[2]

            # Format origin and destination data from database to fit xml file
            origin = rowIntermediate[3]
            origin = origin.strip("(")
            origin = origin.strip(")")
            tmp = origin.split(", ")
            origin = tmp[0] + ', ' + tmp[1]

            destination = rowIntermediate[4]
            destination = destination.strip("(")
            destination = destination.strip(")")
            tmp = destination.split(", ")
            destination = tmp[0] + ', ' + tmp[1]

            tmp = origin.split(", ")
            path_origin = tmp[1] + ',' + tmp[0] + ',0.00'
            tmp = destination.split(", ")
            path_destination = tmp[1] + ',' + tmp[0] + ',0.00'

            # Get the encoded path and transform it into a string
            path_str = ""
            encoded_points = rowIntermediate[6].split(" ")
            decoded_points = []
            numPaths = len(encoded_points)
            j = 0
            while j < numPaths:
                tmp = encoded_points[j]
                decoded_points = PolylineCode.decode_polyline(tmp)
                # decoded_points = polyline.PolylineClass.Par(polyline.PolylineClass.Decode(tmp))
                w = 0
                while w < len(decoded_points):
                    tmp = decoded_points[w]
                    path_str = path_str + str(tmp[1]) + "," + str(tmp[0]) + ",0.0 "
                    w += 1
                j += 1

            path_str = path_str.strip()

            travel_mode = rowIntermediate[5]

            # Create a file to write KML marked language
            file_name = ""
            if part < 10:
                file_name = "C:/Users/Luiz/Google Drive/0 - Projeto Iniciação Científica/IniciacaoCientifica/IniciacaoCientifica/intermediate_KML_file/" + mode + "_from_" + nameorigin + "_to_" + namedestination + "_part_0" + part + ".kml"
            else:
                file_name = "C:/Users/Luiz/Google Drive/0 - Projeto Iniciação Científica/IniciacaoCientifica/IniciacaoCientifica/intermediate_KML_file/" + mode + "_from_" + nameorigin + "_to_" + namedestination + "_part_" + part + ".kml"

            fp = open(file_name, 'w')
            # print(fp, xmlstring)

            # Assembly XML string
            fp.write("<?xml version='1.0' encoding='UTF-8'?>")
            fp.write("<kml xmlns='http://www.opengis.net/kml/2.2'>")
            fp.write("\t<Document>\n")
            fp.write("\t\t<name>Directions from " + origin + " to " + destination + "</name>\n")
            fp.write("\t\t\t<Placemark>\n")
            fp.write("\t\t\t\t<styleUrl>#line-1267FF-5</styleUrl>\n")
            fp.write("\t\t\t\t<name>Directions from " + origin + " to " + destination + "</name>\n")
            fp.write("\t\t\t\t<ExtendedData>\n")
            fp.write("\t\t\t\t</ExtendedData>\n")
            fp.write("\t\t\t\t<LineString>\n")
            fp.write("\t\t\t\t<tessellate>1</tessellate>\n")
            fp.write("\t\t\t\t\t<coordinates>" + path_str + "</coordinates>\n")
            fp.write("\t\t\t\t</LineString>\n")
            fp.write("\t\t\t</Placemark>\n")
            fp.write("\t\t\t<Placemark>\n")
            fp.write("\t\t\t<styleUrl>#icon-503-DB4436</styleUrl>\n")
            fp.write("\t\t\t\t<name>" + origin + "</name>\n")
            fp.write("\t\t\t\t<ExtendedData>\n")
            fp.write("\t\t\t\t</ExtendedData>\n")
            fp.write("\t\t\t\t<description><![CDATA[Origin]]></description>\n")
            fp.write("\t\t\t\t<Point>\n")
            fp.write("\t\t\t\t\t<coordinates>" + path_origin + "</coordinates>\n")
            fp.write("\t\t\t\t</Point>\n")
            fp.write("\t\t\t</Placemark>\n")
            fp.write("\t\t\t<Placemark>\n")
            fp.write("\t\t\t\t<styleUrl>#icon-503-DB4436</styleUrl>\n")
            fp.write("\t\t\t\t<name>" + destination + "</name>\n")
            fp.write("\t\t\t\t<ExtendedData>\n")
            fp.write("\t\t\t\t</ExtendedData>\n")
            fp.write("\t\t\t\t<description><![CDATA[Destination]]></description>\n")
            fp.write("\t\t\t\t<Point>\n")
            fp.write("\t\t\t\t\t<coordinates>" + path_destination + "</coordinates>\n")
            fp.write("\t\t\t\t</Point>\n")
            fp.write("\t\t\t</Placemark>\n")
            fp.write("\t\t\t<Style id='icon-503-DB4436'>\n")
            fp.write("\t\t\t\t<IconStyle>\n")
            fp.write("\t\t\t\t\t<color>ff3644DB</color>\n")
            fp.write("\t\t\t\t\t<scale>1.1</scale>\n")
            fp.write("\t\t\t\t\t<Icon>\n")
            fp.write("\t\t\t\t\t\t<href>http://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>\n")
            fp.write("\t\t\t\t\t</Icon>\n")
            fp.write("\t\t\t\t</IconStyle>\n")
            fp.write("\t\t\t</Style>\n")
            fp.write("\t\t\t<Style id='line-1267FF-5'>\n")
            fp.write("\t\t\t\t<LineStyle>\n")
            fp.write("\t\t\t\t\t<color>ffFF6712</color>\n")
            fp.write("\t\t\t\t\t<width>5</width>\n")
            fp.write("\t\t\t\t</LineStyle>\n")
            fp.write("\t\t\t</Style>\n")
            fp.write("\t</Document>\n")
            fp.write("</kml>\n")

            fp.close()

            part += 1

generateKMLFile(1, "sjc", "sp")

import PolylineCode
import databaseConnection
# import pykml

def generateKMLFile(numRecords, city, state):
    # Connect with database and check if connection have been performed successfully
    con = databaseConnection.connectdb()
    cursor = con.cursor()
    if not con:
        print("Database connection ERROR!")
        exit()

    # Create composed name of table
    tableName = "distances_" + city + "_" + state

    # Create composed name of table where intermediate paths are
    intermediateTableName = "intermiate_distances_" + city + "_" + state

    # Create the name of the foreing key into intermediate table
    idname = "id_distances_" + city + "_" + state

    # Get all the records in database that have not been processed yet
    sql = "SELECT * FROM " + tableName + " WHERE processed=0 ORDER BY id"
    result = cursor.execute(sql)

    i = 0

    # Create an object of class Polyline to decode path
    # polyline = Polyline

    # Create a KML file for each not processed record
    row = cursor.fetchall()
    while row and i <= numRecords:
        id_full_path = row[i][0]
        print(i)

        # Invert coordinates (lat,long to long,lat) for origin and destination. Also removes "(" and ")" from string
        origin = row[i][3]
        origin = origin.strip("(")
        origin = origin.strip(")")
        tmp = origin.split(",")
        origin = tmp[0] + ', ' + tmp[1]
        nameorigin = origin

        destination = row[i][4]
        destination = destination.strip("(")
        destination = destination.strip(")")
        tmp = destination.split(",")
        destination = tmp[0] + ', ' + tmp[1]
        namedestination = destination

        mode = row[i][6].strip()

        path_str = ""

        # Get the encoded path and transform it into a string
        encoded_points = row[i][7].split(" ")
        decoded_points = []
        numPaths = len(encoded_points)
        j = 0
        while j < numPaths:
            tmp = encoded_points[j]
            decoded_points = PolylineCode.decode_polyline(tmp)
            # decoded_points = polylineCode.PolylineClass.Par(polylineCode.PolylineClass.Decode(tmp))
            k = 0
            while k < len(decoded_points):
                tmp = decoded_points[k]
                path_str = path_str + str(tmp[1]) + "," + str(tmp[0]) + ",0.0 "
                k += 1
            j += 1

        path_str = path_str.strip()

        # Create coordinates for origin and destination
        tmp = origin.split(", ")
        path_origin = str(tmp[1]) + ',' + str(tmp[0]) + ',0.00'
        tmp = destination.split(", ")
        path_destination = str(tmp[1]) + ',' + str(tmp[0]) + ',0.00'

        file_name = "/home/luizhenrique/3_Semestre/Iniciacao_Cientifica/intermediate_KML_file/" + mode + "_from_" + nameorigin + "_to_" + namedestination + "_part_00.kml"
        fp = open(file_name, 'w')
        # print(fp, xmlstring)

        # Assembly XML string
        fp.write("<?xml version='1.0' encoding='UTF-8'?>")
        fp.write("<kml xmlns='http://www.opengis.net/kml/2.2'>")
        fp.write("\t<Document>\n")
        fp.write("\t\t<name>Directions from " + origin + " to " + destination + "</name>\n")
        fp.write("\t\t\t<Placemark>\n")
        fp.write("\t\t\t\t<styleUrl>#line-1267FF-5</styleUrl>\n")
        fp.write("\t\t\t\t<name>Directions from " + origin + " to " + destination + "</name>\n")
        fp.write("\t\t\t\t<ExtendedData>\n")
        fp.write("\t\t\t\t</ExtendedData>\n")
        fp.write("\t\t\t\t<LineString>\n")
        fp.write("\t\t\t\t<tessellate>1</tessellate>\n")
        fp.write("\t\t\t\t\t<coordinates>" + path_str + "</coordinates>\n")
        fp.write("\t\t\t\t</LineString>\n")
        fp.write("\t\t\t</Placemark>\n")
        fp.write("\t\t\t<Placemark>\n")
        fp.write("\t\t\t<styleUrl>#icon-503-DB4436</styleUrl>\n")
        fp.write("\t\t\t\t<name>" + origin + "</name>\n")
        fp.write("\t\t\t\t<ExtendedData>\n")
        fp.write("\t\t\t\t</ExtendedData>\n")
        fp.write("\t\t\t\t<description><![CDATA[Origin]]></description>\n")
        fp.write("\t\t\t\t<Point>\n")
        fp.write("\t\t\t\t\t<coordinates>" + path_origin + "</coordinates>\n")
        fp.write("\t\t\t\t</Point>\n")
        fp.write("\t\t\t</Placemark>\n")
        fp.write("\t\t\t<Placemark>\n")
        fp.write("\t\t\t\t<styleUrl>#icon-503-DB4436</styleUrl>\n")
        fp.write("\t\t\t\t<name>" + destination + "</name>\n")
        fp.write("\t\t\t\t<ExtendedData>\n")
        fp.write("\t\t\t\t</ExtendedData>\n")
        fp.write("\t\t\t\t<description><![CDATA[Destination]]></description>\n")
        fp.write("\t\t\t\t<Point>\n")
        fp.write("\t\t\t\t\t<coordinates>" + path_destination + "</coordinates>\n")
        fp.write("\t\t\t\t</Point>\n")
        fp.write("\t\t\t</Placemark>\n")
        fp.write("\t\t\t<Style id='icon-503-DB4436'>\n")
        fp.write("\t\t\t\t<IconStyle>\n")
        fp.write("\t\t\t\t\t<color>ff3644DB</color>\n")
        fp.write("\t\t\t\t\t<scale>1.1</scale>\n")
        fp.write("\t\t\t\t\t<Icon>\n")
        fp.write("\t\t\t\t\t\t<href>http://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>\n")
        fp.write("\t\t\t\t\t</Icon>\n")
        fp.write("\t\t\t\t</IconStyle>\n")
        fp.write("\t\t\t</Style>\n")
        fp.write("\t\t\t<Style id='line-1267FF-5'>\n")
        fp.write("\t\t\t\t<LineStyle>\n")
        fp.write("\t\t\t\t\t<color>ffFF6712</color>\n")
        fp.write("\t\t\t\t\t<width>5</width>\n")
        fp.write("\t\t\t\t</LineStyle>\n")
        fp.write("\t\t\t</Style>\n")
        fp.write("\t</Document>\n")
        fp.write("</kml>\n")

        fp.close()

        # Update database record status to point out that it have already been processed
        # sql2 = "UPDATE " + tableName + " SET processed = '1' WHERE id = " + id_full_path
        # result2 = cursor.execute(sql2)
        i += 1

        # Get intermediate paths from an specific id
        sql2 = "SELECT * FROM " + intermediateTableName + " WHERE " + str(idname) + " = " + str(id_full_path) + " ORDER BY id DESC"
        resultIntermediate = cursor.execute(sql2)
        part = 1

        # For each intermediate part of path, construct a KML file
        rowIntermediate = cursor.fetchall()

        while rowIntermediate:

            # Get data from database for intermediate paths
            distance = rowIntermediate[7]

            duration = rowIntermediate[2]

            # Format origin and destination data from database to fit xml file
            origin = rowIntermediate[3]
            origin = origin.strip("(")
            origin = origin.strip(")")
            tmp = origin.split(", ")
            origin = tmp[0] + ', ' +  tmp[1]

            destination = rowIntermediate[4]
            destination = destination.strip("(")
            destination = destination.strip(")")
            tmp = destination.split(", ")
            destination = tmp[0] + ', ' + tmp[1]

            tmp = origin.split(", ")
            path_origin = tmp[1] + ',' + tmp[0] + ',0.00'
            tmp = destination.split(", ")
            path_destination = tmp[1] + ',' + tmp[0] + ',0.00'

            # Get the encoded path and transform it into a string
            path_str = ""
            encoded_points = rowIntermediate[6].split(" ")
            decoded_points = []
            numPaths = len(encoded_points)
            j = 0
            while j < numPaths:
                tmp = encoded_points[j]
                decoded_points = PolylineCode.decode_polyline(tmp)
                # decoded_points = polyline.PolylineClass.Par(polyline.PolylineClass.Decode(tmp))
                w = 0
                while w < len(decoded_points):
                    tmp = decoded_points[w]
                    path_str = path_str + str(tmp[1]) + "," + str(tmp[0]) + ",0.0 "
                    w += 1
                j += 1

            path_str = path_str.strip()

            travel_mode = rowIntermediate[5]

            # Create a file to write KML marked language
            file_name = ""
            if part < 10:
                file_name = "/home/luizhenrique/3_Semestre/Iniciacao_Cientifica/intermediate_KML_file/" + mode + "_from_" + nameorigin + "_to_" + namedestination + "_part_0" + part + ".kml"
            else:
                file_name = "/home/luizhenrique/3_Semestre/Iniciacao_Cientifica/intermediate_KML_file/" + mode + "_from_" + nameorigin + "_to_" + namedestination + "_part_" + part + ".kml"

            fp = open(file_name, 'w')
            # print(fp, xmlstring)

            # Assembly XML string
            fp.write("<?xml version='1.0' encoding='UTF-8'?>")
            fp.write("<kml xmlns='http://www.opengis.net/kml/2.2'>")
            fp.write("\t<Document>\n")
            fp.write("\t\t<name>Directions from " + origin + " to " + destination + "</name>\n")
            fp.write("\t\t\t<Placemark>\n")
            fp.write("\t\t\t\t<styleUrl>#line-1267FF-5</styleUrl>\n")
            fp.write("\t\t\t\t<name>Directions from " + origin + " to " + destination + "</name>\n")
            fp.write("\t\t\t\t<ExtendedData>\n")
            fp.write("\t\t\t\t</ExtendedData>\n")
            fp.write("\t\t\t\t<LineString>\n")
            fp.write("\t\t\t\t<tessellate>1</tessellate>\n")
            fp.write("\t\t\t\t\t<coordinates>" + path_str + "</coordinates>\n")
            fp.write("\t\t\t\t</LineString>\n")
            fp.write("\t\t\t</Placemark>\n")
            fp.write("\t\t\t<Placemark>\n")
            fp.write("\t\t\t<styleUrl>#icon-503-DB4436</styleUrl>\n")
            fp.write("\t\t\t\t<name>" + origin + "</name>\n")
            fp.write("\t\t\t\t<ExtendedData>\n")
            fp.write("\t\t\t\t</ExtendedData>\n")
            fp.write("\t\t\t\t<description><![CDATA[Origin]]></description>\n")
            fp.write("\t\t\t\t<Point>\n")
            fp.write("\t\t\t\t\t<coordinates>" + path_origin + "</coordinates>\n")
            fp.write("\t\t\t\t</Point>\n")
            fp.write("\t\t\t</Placemark>\n")
            fp.write("\t\t\t<Placemark>\n")
            fp.write("\t\t\t\t<styleUrl>#icon-503-DB4436</styleUrl>\n")
            fp.write("\t\t\t\t<name>" + destination + "</name>\n")
            fp.write("\t\t\t\t<ExtendedData>\n")
            fp.write("\t\t\t\t</ExtendedData>\n")
            fp.write("\t\t\t\t<description><![CDATA[Destination]]></description>\n")
            fp.write("\t\t\t\t<Point>\n")
            fp.write("\t\t\t\t\t<coordinates>" + path_destination + "</coordinates>\n")
            fp.write("\t\t\t\t</Point>\n")
            fp.write("\t\t\t</Placemark>\n")
            fp.write("\t\t\t<Style id='icon-503-DB4436'>\n")
            fp.write("\t\t\t\t<IconStyle>\n")
            fp.write("\t\t\t\t\t<color>ff3644DB</color>\n")
            fp.write("\t\t\t\t\t<scale>1.1</scale>\n")
            fp.write("\t\t\t\t\t<Icon>\n")
            fp.write("\t\t\t\t\t\t<href>http://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>\n")
            fp.write("\t\t\t\t\t</Icon>\n")
            fp.write("\t\t\t\t</IconStyle>\n")
            fp.write("\t\t\t</Style>\n")
            fp.write("\t\t\t<Style id='line-1267FF-5'>\n")
            fp.write("\t\t\t\t<LineStyle>\n")
            fp.write("\t\t\t\t\t<color>ffFF6712</color>\n")
            fp.write("\t\t\t\t\t<width>5</width>\n")
            fp.write("\t\t\t\t</LineStyle>\n")
            fp.write("\t\t\t</Style>\n")
            fp.write("\t</Document>\n")
            fp.write("</kml>\n")

            fp.close()

            part += 1

generateKMLFile(1, "sjc", "sp")
