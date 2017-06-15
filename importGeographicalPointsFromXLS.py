import excelReader
from gPointConverter import GPointerConverteClass

def importGeographicalPointsFromXLS(fileName):
    # Create a path for input file (input files are stored into folder INPUT)
    path = "input/" + fileName + ".xls"

    # Use py class to create an object whose contains table information
    data = excelReader.Spreadsheet_Excel_Reader()

    # Use py class to convert between UTM to lat/long
    converter = GPointerConverteClass

    # Get number of rows of table
    sheet_index = 0
    rows = 56 # data.rowcount(sheet_index)

    # Create a vector named coordenates where each line is a par of [long,lat]
    coordinates = []
    i = 2
    while i <= rows:
        xcentroid = data.xValue(i)
        xcentroid = float(xcentroid[0])
        ycentroid = data.yValue(i)
        ycentroid = float(ycentroid[0])
        tt = converter.convertUtmToLatLng(xcentroid, ycentroid, 23)
        lat = tt[0]
        long = tt[1]
        coordinates.append([long, lat])
        i += 1
    return coordinates
