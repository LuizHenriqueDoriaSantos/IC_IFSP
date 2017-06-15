import psycopg2

def connectdb():
    host = "localhost"
    port = "5432"
    dbName = "hazard-mobility"
    user = "postgres"
    password = "postgres"

    query = "host=" + host + " port=" + port + " dbname=" + dbName + " user=" + user + " password=" + password
    handle = psycopg2.connect(query)
    return handle
