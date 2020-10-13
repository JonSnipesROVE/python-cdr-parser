#! /usr/bin/python3

##############################
## Jon Snipes   |   ROVE    ##
## Parse CDR via CSV export ##
##############################

import csv
import time
import argparse
import re
from os import path
import sqlite3 as db

#####################
## Start Functions ##
#####################

# parse command line arguments
def parse_arguments():
  ## Parge Command Line Arguments
  parser = argparse.ArgumentParser(description='What to do from here:')
  parser.add_argument("-d", action='store_true',default=False, help="Enable Debuging")
  parser.add_argument("-f", default=None, help="CDR File Location")
  parser.add_argument("-db", default=None, help="CDR DB Location")

  return parser.parse_args()

def create_table(cdrCSV):
	#Build table syntax
	colList = []
	colQues = "?," * (len(colList) - 1) + "?"
	cdrData = []
	headerRow = True

	#create table
	with cdrDB:
		with open(cdrCSV,'r') as fin:
			# csv.DictReader uses first line in file for column headings by default
			dr = csv.DictReader(fin) # comma is default delimiter
			for row in dr:
				cdrRow = ()
				if headerRow is True:
					headerRow = False
					for col in row:
						colList.append(col)
					sql = f"CREATE TABLE cdr ({' varchar(128), '.join(colList)} varchar(128));"
					cdrDB.execute(sql)

				else:
					for col in row:
						cdrRow = cdrRow +( row[col] ,)
					sql = f"INSERT INTO cdr ({','.join(colList)}) VALUES {cdrRow};"
					cdrDB.execute(sql)

		cdrDB.commit()

	return True

def sql_query(sql,delimiter = "tab"):
	with cdrDB:
		cur = cdrDB.cursor()
		try:
			data = cur.execute(sql)    
		except db.Error as err:
			print(f"SQL Error!  Try again. {err}")
			return False
		else:
			if re.match("select",sql):
				rows = cur.fetchall()
				if len(rows) == 0:
					print("no results")
				else:
					for row in rows:
						header = ""
						for col in dict(row):
							if delimiter == "tab":
								header = header + '{:24.24}'.format(col) + "  "
							else:
								if header == "":
									header = col
								else:
									header = header + "," + col
						break
					print(header)
					for row in rows:
						rowData = ""
						for cell in row:
							if delimiter == "tab":
								rowData = rowData + '{:24.24}'.format(str(cell)) + "  "
							else:
								if rowData == "":
									rowData = cell
								else:
									rowData = rowData + "," + cell
						print(rowData)

			else:
				print("Only supports select statements for now.")
		return True

################
## Start MAIN ##
################
def main():
	delim = "tab"
	print("table name is cdr")
	while True:
		sql = input("sql> ")
		if sql == "":
			True
		elif sql == "exit" or sql == "quit":
			break
		elif sql == "config csv":
			delim = "csv"
		elif sql == "config tab":
			delim = "tab"
		else:
			sql_query(sql,delim)

if __name__ == '__main__':
	try:
		timestamp = time.time()
		args = parse_arguments()

		if args.db is not None and path.isfile(f"{args.db}"):
			cdrDB = db.connect(args.db)
			cdrDB.row_factory = db.Row

		elif args.f is not None and path.isfile(args.f):
			if path.isfile(f"{args.f}.db"):
				useCDRDB = input("DB Path exists.  Use this DB? [y/n]")
				if useCDRDB == "y" or useCDRDB == "":
					cdrDB = db.connect(f"{args.f}.db")
					cdrDB.row_factory = db.Row

				else: 
					quit()
			else:
				cdrDB = db.connect(f"{args.f}.db")
				cdrDB.row_factory = db.Row
				if create_table(args.f):
					print("CSV file loaded to DB.")
				else:
					print("Error loading CSV.")
					quit()

		else:
			print("Must supply a DB or a CSV file to get started")
			quit()
		
		main()

	except KeyboardInterrupt:
		print('\n')
		pass

	finally:
		print()
