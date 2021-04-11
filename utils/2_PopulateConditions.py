""" 2_PopulateConditions.py

Populates initial data in a local MySQL db needed for user study
as part of Honours research project.

"""
__author__ = "Christopher Chow"
__version__ = "0.1"
__created__ = "11 April 2017"

import pymysql.cursors
import csv
import os

# Connect to the database
connection = pymysql.connect(
    host="localhost",
    user="alpha",
    passwd="***REMOVED***",
    db="alpha",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
)

try:
    with connection.cursor() as cursor:

        # Populate Users table

        order = ["A", "B", "C", "D", "E"]
        target = ["sec", "dis", "com", "psy"]
        for x in target:
            for y in order:
                sql = "INSERT INTO `Users` (`order`, `target`) VALUES (%s, %s)"
                cursor.execute(sql, (y, x))

        # Commit to save changes into db
        connection.commit()

finally:
    connection.close()

connection = pymysql.connect(
    host="localhost",
    user="alpha",
    passwd="***REMOVED***",
    db="alpha",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
)

try:
    with connection.cursor() as cursor:

        # Add the document orders from order.csv

        file_dir = os.path.dirname(os.path.abspath(__file__))
        order_file = os.path.join(file_dir, "order.csv")

        with open(order_file, "r") as infile:
            documents = csv.reader(infile)

            for row in documents:
                data = ()
                sql = "INSERT INTO `Orders` (`order`, `doc_"

                for x in range(1, (len(row) - 1)):
                    sql = sql + str(x) + "`, `doc_"

                sql = sql + "40`) VALUES ("

                for y in range(1, len(row)):
                    sql = sql + "%s, "

                sql = sql + "%s)"

                for y in range(0, len(row)):
                    data = data + (row[y],)

                cursor.execute(sql, data)

        # Commit to save changes
        connection.commit()

finally:
    connection.close()
