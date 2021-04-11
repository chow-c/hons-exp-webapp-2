""" 1_GenerateTables.py

Creates tables in a local MySQL db needed for user study
as part of Honours research project.

"""
__author__ = "Christopher Chow"
__version__ = "0.1"
__created__ = "11 April 2017"

import pymysql.cursors
import csv
import os


# CREATE ORDERS TABLE (FROM THE LATIN SQUARE)
try:
    # Connect to the database
    connection = pymysql.connect(
        host="localhost",
        user="alpha",
        passwd="alpha",
        db="charlie",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    with connection.cursor() as cursor:

        # Delete the table if it already exists
        # NOTE: You should not be running this script multiple times - it is a first-time use to create the necessary tables for the Alpha experiment
        drop = "DROP TABLE IF EXISTS `Orders`"
        cursor.execute(drop)

        connection.commit()

        sql = "CREATE TABLE `Orders` (`oid` int(4) NOT NULL AUTO_INCREMENT, `order` ENUM('A','B','C','D','E'), "
        dir = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(dir, "order.csv")

        with open(file, "r") as infile:
            documents = csv.reader(infile)
            header = next(documents)

            for x in range(1, (len(header))):
                sql = sql + "`doc_" + str(x) + "` INT(4), "

        sql = (
            sql
            + "PRIMARY KEY (`oid`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1"
        )

        cursor.execute(sql)

        # Commit to save changes
        connection.commit()

finally:
    connection.close()

    # CREATE USERS TABLE
try:
    connection = pymysql.connect(
        host="localhost",
        user="alpha",
        passwd="alpha",
        db="charlie",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    with connection.cursor() as cursor:

        # Delete the table if it already exists
        # NOTE: You should not be running this script multiple times - it is a first-time use to create the necessary tables for the Alpha experiment
        drop = "DROP TABLE IF EXISTS `Users`"
        cursor.execute(drop)

        connection.commit()

        # Create a new Users Table
        sql = "CREATE TABLE `Users` (`uid` int(4) NOT NULL AUTO_INCREMENT, `age` ENUM('0-19', '20-29', '30-39', '40+'), `gender` ENUM('Male', 'Female'), `degree` TEXT, `vision` BOOLEAN, `order` ENUM('A','B','C','D','E', 'F'), `target` ENUM('sec', 'dis', 'com', 'psy'), `familiarity` ENUM('0','1','2','3','4','5'), `initial_stress` ENUM('0','1','2','3','4','5'), `final_stress` ENUM('0','1','2','3','4','5'), `time` DATETIME, `complete` BOOLEAN NOT NULL DEFAULT FALSE, PRIMARY KEY (`uid`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1"
        cursor.execute(sql)

        # Commit to save changes
        connection.commit()

finally:
    connection.close()

    # CREATE RESULTS TABLE
try:
    connection = pymysql.connect(
        host="localhost",
        user="alpha",
        passwd="alpha",
        db="charlie",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    with connection.cursor() as cursor:

        # Delete the table if it already exists
        # NOTE: You should not be running this script multiple times - it is a first-time use to create the necessary tables for the Alpha experiment
        drop = "DROP TABLE IF EXISTS `Results`"
        cursor.execute(drop)

        connection.commit()

        # Create a new Users Table
        sql = "CREATE TABLE `Results` (`rid` int(4) NOT NULL AUTO_INCREMENT, `uid` INT(4), `target` ENUM('sec', 'dis', 'com', 'psy'), `doc_number` INT(4), `decision` BOOLEAN, `doc_sec` TINYINT, `doc_dis` TINYINT, `doc_com` TINYINT, `doc_psy` TINYINT, `time_spent` TEXT, `confidence` TINYINT, `score` TINYINT, PRIMARY KEY (`rid`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1"
        cursor.execute(sql)

        # Commit to save changes
        connection.commit()

finally:
    connection.close()
