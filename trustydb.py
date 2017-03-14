#!/usr/bin/env python

import MySQLdb

# create table reminders(reminder_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,reminder_name TEXT,reminder_data TEXT);
'''
TABLE FORMATS

REMINDERS:
R_ID (PKEY) | R_NAME (TEXT) | R_DATA (TEXT) | R_USER (U_ID)

USERS:
U_ID (PKEY) | U_NAME (TEXT) | U_AGE (INT) | U_HOME (TEXT)
'''    


class TrustyDb(object):

    def __init__(self,host='',user='',pw='',db=''):
        self.host = host
        self.user = user
        self.pw = pw
        self.db = db


    '''
    function: create_users
    description: creates the USERS table
    '''
    def create_users(self):

        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        cursor = db.cursor()

        cursor.execute('DROP IF TABLE EXISTS USERS')

        raw_users_query = """CREATE TABLE USERS ( 
                            U_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            U_NAME TEXT,
                            U_AGE INT,
                            U_HOME TEXT )"""
        cursor.execute(raw_users_query)
        db.close()


    '''
    function: create_reminders
    description: creates the REMINDERS table
    '''
    def create_reminders(self):

        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        cursor = db.cursor()

        cursor.execute('DROP IF TABLE EXISTS REMINDERS')

        raw_reminders_query = """CREATE TABLE REMINDERS ( 
                                 R_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                 R_NAME TEXT,
                                 R_DATA TEXT,
                                 R_USER INT,
                                 FOREIGN KEY (R_USER) REFERENCES USERS(U_ID) )"""
        cursor.execute(raw_reminders_query)
        db.close()


    '''
    function: add_reminder
    description: adds a reminder to the reminder table
    '''
    def add_reminder(self,r_name,r_data,r_usr):

        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        add_reminder_query = """INSERT INTO REMINDERS (
                                R_NAME, R_DATA, R_USER ) VALUES (
                                '%s', '%s', (SELECT U_ID FROM USERS WHERE
                                U_NAME = '%s') ) """ % (r_name, r_data, r_usr)

        print('Query to add {}'.format(add_reminder_query))

        try:
            cursor.execute(add_reminder_query)
            db.commit()
            print('Added reminder successfully!')

        except:
            print('Failed to add reminder!')
            db.rollback()

        db.close()


    # TODO
    '''
    function: get_reminders
    description: fetches reminders given the U_ID
    '''
    def get_reminders(self):
        return 0

