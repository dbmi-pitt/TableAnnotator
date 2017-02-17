# -*- coding: utf-8 -*-
import csv
import mysql.connector
from mysql.connector import Error
import json
import datetime
from sets import Set
import sys
import codecs

#reload(sys)  
#sys.setdefaultencoding('utf8')

#1. create config file: "DB-config.txt"

db_config_files = "DB-config.txt"
hostname = 'localhost'

#connect database
#input: config file, database name
#return: database connection
def connect_DB(db_config_files, database):
	dbconfig = file = open(db_config_files)
	if dbconfig:
		for line in dbconfig:
			if "USERNAME" in line:
				username = line[(line.find("USERNAME=")+len("USERNAME=")):line.find(";")]
			elif "PASSWORD" in line:
				password = line[(line.find("PASSWORD=")+len("PASSWORD=")):line.find(";")]
		myConnection = mysql.connector.connect(host=hostname, user=username, password=password, charset='utf8', use_unicode=True)	
		print("Database connection created")
	else:
		print "Configuration file is not found: " + dbconfig

	return myConnection


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


class EffectInTable:
	'{tableID:, articleID:, productLabel:, tableInfo:{cellID:, cellContent:}}'

	def __init__(self, tableID):
		self.tableID = tableID
		self.articleID = ""
		self.productLabel = ""
		self.tableInfo = {}

	def displayEffect(self):
		print "tableID: %s, articleID: %s, productLabel: %s" % (self.tableID, self.articleID, self.productLabel)


def exactEffect(conn, CUIs):
	effectMap = {}
	allTable = ""
	cur = conn.cursor()
	#get relevant tables ('effect' CUI exits in header)
	cur.execute("SELECT DISTINCT Cell.Table_idTable " +
		"FROM AMIA_TBI_table_db_spls.Cell, AMIA_TBI_table_db_spls.Annotation, AMIA_TBI_table_db_spls.CellRoles, AMIA_TBI_table_db_spls.CellRole, AMIA_TBI_table_db_spls.ArtTable " +
		"WHERE Cell.idCell = Annotation.Cell_idCell AND Cell.idCell = CellRoles.Cell_idCell AND CellRoles.CellRole_idCellRole = CellRole.idCellRole AND Cell.Table_idTable = ArtTable.idTable " +
		"AND ArtTable.Section = '34073-7' " +
		"AND Annotation.AnnotationID IN (%s) AND (CellRole.CellRoleName = 'Header' OR Cell.RowN = 0);" % (CUIs))
	for result in cur.fetchall():
		effectMap[result[0]] = EffectInTable(result[0])
		allTable += str(result[0]) + ","

	#get articleID, productLabel of these tables
	cur.execute("SELECT ArtTable.idTable, Article.SpecId, PL.fullName " + 
		"FROM AMIA_TBI_table_db_spls.Article, AMIA_TBI_table_db_spls.ArtTable, linkedSPLs.structuredProductLabelMetadata PL " + 
		"WHERE Article.idArticle = ArtTable.Article_idArticle AND Article.SpecId = PL.setId " + 
		"AND ArtTable.idTable IN (%s);" % (allTable[:-1]))
	for result in cur.fetchall():
		effectMap[result[0]].articleID = result[1]
		effectMap[result[0]].productLabel = result[2]

	#get relevant tableInfo from these tables (use HeaderRef)
	for key, value in effectMap.iteritems():
		cur.execute("SELECT Cell.CellID, Cell.Content, CellRole.CellRoleName, Cell.WholeStub, Cell.WholeSuperRow, ArtTable.StructureType FROM AMIA_TBI_table_db_spls.Cell, AMIA_TBI_table_db_spls.CellRoles, AMIA_TBI_table_db_spls.CellRole, AMIA_TBI_table_db_spls.ArtTable " +
			"WHERE ArtTable.idTable = Cell.Table_idTable AND Cell.idCell = CellRoles.Cell_idCell AND CellRole.idCellRole = CellRoles.CellRole_idCellRole AND Cell.Table_idTable = %s AND Cell.ColumnN IN (SELECT DISTINCT ColumnN FROM AMIA_TBI_table_db_spls.Cell, AMIA_TBI_table_db_spls.Annotation, AMIA_TBI_table_db_spls.CellRoles, AMIA_TBI_table_db_spls.CellRole WHERE Cell.idCell = Annotation.Cell_idCell AND Cell.idCell = CellRoles.Cell_idCell AND CellRoles.CellRole_idCellRole = CellRole.idCellRole AND Annotation.AnnotationID IN (%s) AND (CellRole.CellRoleName = 'Header' OR Cell.RowN = 0) AND Cell.Table_idTable = %s);" % (key, CUIs, key))
		for result in cur.fetchall():
			temp = [unicode(result[1]).strip(), unicode(result[2]), unicode(result[3]).strip(), unicode(result[4]).strip(), unicode(result[5])];
			effectMap[key].tableInfo[result[0]] = temp;

	return effectMap


def output(effectMap):
	with open('result.csv', 'w') as outfile:
		fieldnames = ['articleID', 'tableID', 'productLabel', 'WholeStub', 'cellID', 'cellRole', 'cellContent', 'WholeSuperRow', 'StructureType']
		writer = csv.writer(outfile, delimiter = ',')
		writer.writerow(fieldnames)
		for key, value in effectMap.iteritems():
			for cellKey, cellValue in value.tableInfo.iteritems():
				if cellValue[2] == cellValue[0]:
					cellValue[2] = 'NA'
				row = [value.articleID, value.tableID, value.productLabel, cellValue[2].encode('UTF-8'), cellKey, cellValue[1].encode('UTF-8'), cellValue[0].encode('UTF-8'), cellValue[3].encode('UTF-8'), cellValue[4].encode('UTF-8')]
				writer.writerow(row)

def main():

	#get CUI -todo
	CUIs = "'C1280500', 'C2348382'"
	
	#connect database
	print("[info] connect mySQL ...")
	UPCI_conn = connect_DB(db_config_files, "UPCI_table_db_spls")

	#extract effect
	result = {}
	result = exactEffect(UPCI_conn, CUIs)

	#output to csv
	output(result)

	UPCI_conn.close()
	print("[info] completed ...")


if __name__ == '__main__':
	main()


