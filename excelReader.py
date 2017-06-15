import databaseConnection
import csv
# import xlrd


postgre = databaseConnection.connectdb()
cursor = postgre.cursor()


# Usar o caminho do arquivo zonas-trafego-sjc-sp-csv.csv
wb1 = csv.reader(open("/home/luizhenrique/3_Semestre/IniciacaoCientifica/Excel/zonas-trafego-sjc-sp-csv.CSV"))
# wb2 = xlrd.open_workbook("/home/luiz/IniciacaoCientifica/zonas-trafego-sjc-sp.xls")

# salva no banco de dados os dados da tabela do excel
for row in wb1:
    cursor.execute("INSERT INTO excel (zonatrafego, pop_ibge, dom_ibge, macrozona, nome_zt, pop_od, dom_od, perc_pop, perc_dom, area_km, x_centroid, y_centroid, pop_area) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

postgre.commit()
cursor.close()

class Spreadsheet_Excel_Reader:

    sheets = []
    colnames = []

    def getCol(self, col):
        if (isinstance(col,str)):
            col = col.lower()
        if (col in self.colnames):
            col = self.colnames[col]
        return col

    def rowcount(self, sheet):
        return self.sheets[sheet]['numRows']

    def val(self, row, col, sheet = 0):
        col = self.getCol(col)
        if row in self.sheets[sheet]['cells'] and col in self.sheets[sheet]['cells'][row]:
            return self.sheets[sheet]['cells'][row][col]
        else:
            return ""

    def xValue(self, row):
        postgres = databaseConnection.connectdb()
        cursor = postgres.cursor()
        cursor.execute("SELECT x_centroid FROM excel where id = %d" %row)
        return cursor.fetchone()

    def yValue(self, row):
        postgre = databaseConnection.connectdb()
        cursor = postgre.cursor()
        cursor.execute("SELECT y_centroid FROM excel where id = %d" %row)
        return cursor.fetchone()