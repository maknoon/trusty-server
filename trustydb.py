#!/usr/bin/env python

import MySQLdb
from datetime import datetime

'''
TABLE FORMATS

USERS:
U_ID (PKEY) | U_NAME VARCHAR(32) | U_AGE (INT) | U_HOME_ADDR VARCHAR(128)

REMINDERS:
R_ID (PKEY) | R_NAME VARCHAR(32) | R_DATA VARCHAR(128) | R_UNAME VARCHAR(32) | R_UID (U_ID)

LOCATIONS:
L_ID (PKEY) | L_UNAME VARCHAR(32) | L_LON FLOAT(10,7) | L_LAT FLOAT(10,7) | L_DT DATETIME | L_UID INT

'''


class TrustyDb(object):

    def __init__(self,host='',user='',pw='',db=''):
        self.host = host
        self.user = user
        self.pw = pw
        self.db = db


    '''
    function: reset_db
    description: delete all tables in trustyDb and recreate
    notes: need to do in this order bc the tables are key-dependent
    '''
    def reset_db(self):
        trusty = MySQLdb.connect(host=self.host,
                                 user=self.user,
                                 passwd=self.pw,
                                 db=self.db)
        cursor = trusty.cursor()

        cursor.execute('DROP TABLE IF EXISTS REMINDERS')
        cursor.execute('DROP TABLE IF EXISTS LOCATIONS')
        cursor.execute('DROP TABLE IF EXISTS USERS')

        raw_users_query = """CREATE TABLE USERS (
                             U_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                             U_NAME VARCHAR(32),
                             U_AGE INT,
                             U_HOME_ADDR VARCHAR(128) )"""
        cursor.execute(raw_users_query)
        print('Created new USERS table in {}'.format(self.db))

        raw_reminders_query = """CREATE TABLE REMINDERS (
                                 R_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                 R_NAME VARCHAR(32),
                                 R_DATA VARCHAR(128),
                                 R_UNAME VARCHAR(32),
                                 R_UID INT,
                                 FOREIGN KEY (R_UID) REFERENCES USERS(U_ID) )"""
        cursor.execute(raw_reminders_query)
        print('Created new REMINDERS table in {}'.format(self.db))

        raw_location_query = """CREATE TABLE LOCATIONS (
                                L_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                L_UNAME VARCHAR(32),
                                L_LON FLOAT(10,7),
                                L_LAT FLOAT(10,7),
                                L_DT DATETIME,
                                L_UID INT,
                                FOREIGN KEY (L_UID) REFERENCES USERS(U_ID) )"""
        cursor.execute(raw_location_query)
        print('Created new LOCATIONS table in {}'.format(self.db))

        trusty.close()


    '''
    function: add_user
    description: adds a user to the users table
    '''
    def add_user(self,u_name,u_age,u_addr):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        add_user_query = """INSERT INTO USERS (
                            U_NAME, U_AGE, U_HOME_ADDR ) VALUES (
                            '%s', '%s', '%s' )""" % (u_name, u_age, u_addr)

        print('Query to add {}'.format(add_user_query))

        try:
            cursor.execute(add_user_query)
            db.commit()
            print('Added user successfully!')

        except:
            print('Failed to add user!')
            db.rollback()

        db.close()


    '''
    function: get_user
    description: fetches user given the user_name
    '''
    def get_user(self,u_name):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        get_user_query = """SELECT * FROM USERS WHERE
                            U_NAME = '%s'""" % u_name

        print('Query to fetch {}'.format(get_user_query))

        try:
            cursor.execute(get_user_query)
            data = cursor.fetchone()
            print('U_ID: {0} | U_NAME: {1} | U_AGE: {2} | \
                   U_HOME_ADDR: {3}'.format(data[0], data[1],
                    data[2], data[3]))

            db.close()
            return data

        except:
            print('Failed to fetch user!')

            db.close()
            return 0


    '''
    function: add_reminder
    description: adds a reminder to the reminders table
    '''
    def add_reminder(self,r_name,r_data,r_usr):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        add_reminder_query = """INSERT INTO REMINDERS (
                                R_NAME, R_DATA, R_UNAME, R_UID ) VALUES (
                                '%s', '%s', '%s', (SELECT U_ID FROM USERS WHERE
                                U_NAME = '%s') )""" % (r_name, r_data, r_usr, r_usr)

        print('Query to add {}'.format(add_reminder_query))

        try:
            cursor.execute(add_reminder_query)
            db.commit()
            print('Added reminder successfully!')

        except:
            print('Failed to add reminder!')
            db.rollback()

        db.close()


    '''
    function: get_reminders
    description: fetches reminders given the user_name
    '''
    def get_reminders(self,u_name):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        get_reminders_query = """SELECT * FROM REMINDERS WHERE
                                 R_UID = (SELECT U_ID FROM USERS WHERE
                                 U_NAME = '%s')""" % u_name

        print('Query to fetch {}'.format(get_reminders_query))

        try:
            cursor.execute(get_reminders_query)
            rems = cursor.fetchall()
            for row in rems:
                print('R_ID: {0} | R_NAME: {1} | R_DATA: {2}'.format(
                    row[0], row[1], row[2]))

            db.close()
            return rems

        except:
            print('Failed to fetch reminders!')

            db.close()
            return 0

    '''
    function: add_location
    description: adds a reminder to the reminders table
    '''
    def add_location(self,lon,lat,u_name):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        dt = str(datetime.now())

        add_location_query = """INSERT INTO LOCATIONS (
                                L_UNAME, L_LON, L_LAT, L_DT, L_UID ) VALUES (
                                '%s', '%s', '%s', '%s',
                                (SELECT U_ID FROM USERS WHERE U_NAME = '%s')
                                 )""" % (u_name, lon, lat, dt, u_name)

        print('Query to add {}'.format(add_location_query))

        try:
            cursor.execute(add_location_query)
            db.commit()
            print('Added location data successfully!')

        except:
            print('Failed to add location data!')
            db.rollback()

        db.close()


    '''
    function: get_locations
    description: fetches locations given the user_name
    '''
    def get_locations(self,u_name):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        get_locations_query = """SELECT * FROM LOCATIONS WHERE L_UID = 
                                (SELECT U_ID FROM USERS WHERE U_NAME = '%s')""" % u_name

        print('Query to fetch {}'.format(get_locations_query))

        try:
            cursor.execute(get_locations_query)
            locs = cursor.fetchall()
            for loc in locs:
                print('L_ID: {0} | L_UNAME: {1} | L_LON: {2} | L_LAT: {3} \
                     | L_DT: {4} | L_UID: {5}'.format(loc[0], loc[1],
                       loc[2], loc[3], loc[4], loc[5]))

            db.close()
            return locs

        except:
            print('Failed to fetch locations!')

            db.close()
            return 0


