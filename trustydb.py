#!/usr/bin/env python

import MySQLdb

# create table reminders(reminder_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,reminder_name TEXT,reminder_data TEXT);
'''
TABLE FORMATS


USERS:
U_ID (PKEY) | U_NAME (TEXT) | U_AGE (INT) | U_HOME_ADDR (TEXT)

REMINDERS:
R_ID (PKEY) | R_NAME (TEXT) | R_DATA (TEXT) | R_USER (TEXT) | R_UID (U_ID)

'''    


class TrustyDb(object):

    def __init__(self,host='',user='',pw='',db=''):
        self.host = host
        self.user = user
        self.pw = pw
        self.db = db


    '''
    function: reset_db
    description: delete all tables in trustyDb
    notes: need to do in this order bc the tables are key-dependent
    '''
    def reset_db(self):
        trusty = MySQLdb.connect(host=self.host,
                                 user=self.user,
                                 passwd=self.pw,
                                 db=self.db)
        cursor = trusty.cursor()

        cursor.execute('DROP TABLE IF EXISTS REMINDERS')
        cursor.execute('DROP TABLE IF EXISTS USERS')

        raw_users_query = """CREATE TABLE USERS ( 
                             U_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                             U_NAME TEXT,
                             U_AGE INT,
                             U_HOME_ADDR TEXT )"""
        cursor.execute(raw_users_query)
        print('Created new USERS table in {}'.format(self.db))

        raw_reminders_query = """CREATE TABLE REMINDERS ( 
                                 R_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                 R_NAME TEXT,
                                 R_DATA TEXT,
                                 R_USER TEXT,
                                 R_UID INT,
                                 FOREIGN KEY (R_UID) REFERENCES USERS(U_ID) )"""
        cursor.execute(raw_reminders_query)
        print('Created new REMINDERS table in {}'.format(self.db))

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
                                R_NAME, R_DATA, R_USER, R_UID ) VALUES (
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
            results = cursor.fetchall()
            for row in results:
                print('R_ID: {0} | R_NAME: {1} | R_DATA: {2}'.format(
                    row[0], row[1], row[2]))

            db.close()
            return results

        except:
            print('Failed to fetch reminders!')

            db.close()
            return 0

