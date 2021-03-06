#!/usr/bin/env python

import strings
import MySQLdb
from datetime import datetime

'''
TABLE FORMATS

USERS:
U_ID (PKEY) | U_NAME VARCHAR(32) | U_AGE (INT) | U_HOME_ADDR VARCHAR(128) | U_PHONE_NUMBER VARCHAR(32)

REMINDERS:
R_ID (PKEY) | R_NAME VARCHAR(32) | R_DATA VARCHAR(128) | R_DUE DATETIME | R_UNAME VARCHAR(32) | R_UID INT (FK U_ID)

LOCATIONS:
L_ID (PKEY) | L_UNAME VARCHAR(32) | L_LON FLOAT(10,7) | L_LAT FLOAT(10,7) | L_DT DATETIME | L_UID INT (FK U_ID)

AUTH:
A_ID (PKEY) | A_NAME VARCHAR(32) UNIQUE | A_PASS BINARY(60) | A_TOKEN VARCHAR(256) | A_UID INT (FK U_ID)

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

        drop = 'DROP TABLE IF EXISTS {}'
        cursor.execute(drop.format('AUTH'))
        cursor.execute(drop.format('REMINDERS'))
        cursor.execute(drop.format('LOCATIONS'))
        cursor.execute(drop.format('USERS'))

        raw_users_query = """CREATE TABLE USERS (
                             U_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                             U_NAME VARCHAR(32),
                             U_AGE INT,
                             U_HOME_ADDR VARCHAR(128),
                             U_PHONE_NUMBER VARCHAR(32) )"""
        cursor.execute(raw_users_query)
        print((strings.create_table).format('USERS',self.db))

        raw_reminders_query = """CREATE TABLE REMINDERS (
                                 R_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                 R_NAME VARCHAR(60),
                                 R_DATA VARCHAR(128),
                                 R_DUE DATETIME,
                                 R_UNAME VARCHAR(32),
                                 R_UID INT,
                                 FOREIGN KEY (R_UID) REFERENCES USERS(U_ID) )"""
        cursor.execute(raw_reminders_query)
        print((strings.create_table).format('REMINDERS',self.db))

        raw_location_query = """CREATE TABLE LOCATIONS (
                                L_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                L_UNAME VARCHAR(32),
                                L_LON FLOAT(10,7),
                                L_LAT FLOAT(10,7),
                                L_DT DATETIME,
                                L_UID INT,
                                FOREIGN KEY (L_UID) REFERENCES USERS(U_ID) )"""
        cursor.execute(raw_location_query)
        print((strings.create_table).format('LOCATIONS',self.db))

        raw_auth_query = """CREATE TABLE AUTH (
                             A_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                             A_NAME VARCHAR(32) NOT NULL UNIQUE,
                             A_PASS BINARY(60),
                             A_TOKEN VARCHAR(256),
                             A_UID INT,
                             FOREIGN KEY (A_UID) REFERENCES USERS(U_ID) )"""
        cursor.execute(raw_auth_query)
        print((strings.create_table).format('AUTH',self.db))

        trusty.close()


    ## === USERS ===============================================================

    '''
    function: add_user
    description: adds a user to the users table
    returns: the primary key (u_id) of the inserted user (0 if unsuccessful)
    '''
    def add_user(self,u_name,u_age,u_addr,u_pnum):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        inserted = 0
        add_user_query = """INSERT INTO USERS (
                            U_NAME, U_AGE, U_HOME_ADDR, U_PHONE_NUMBER ) VALUES (
                            '%s', '%s', '%s', '%s' )""" % (u_name, u_age, u_addr, u_pnum)
        print(add_user_query)

        try:
            cursor.execute(add_user_query)
            db.commit()
            print((strings.add_success).format('user',u_name,'USERS'))
            inserted = cursor.lastrowid
        except:
            print((strings.add_failed).format('user',u_name,'USERS'))
            db.rollback()

        db.close()

        return inserted


    '''
    function: get_user
    description: fetches user given the user_id
    '''
    def get_user(self,u_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        get_user_query = """SELECT * FROM USERS WHERE
                            U_ID = '%s'""" % u_id
        print(get_user_query)

        try:
            cursor.execute(get_user_query)
            data = cursor.fetchone()
            print((strings.get_success).format(u_id,'USERS'))
            print('U_ID: {0} | U_NAME: {1} | U_AGE: {2} |\
             U_HOME_ADDR: {3} | U_PHONE_NUMBER: {4}'.format(data[0], data[1], data[2], data[3], data[4]))
            db.close()

            return data

        except:
            print((strings.get_failed).format(u_id,'USERS'))
            db.close()

            return 0

    '''
    function: get_user_by_name
    description: fetches user given the user_name
    '''
    def get_user_by_name(self,u_name):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        get_user_query = """SELECT * FROM USERS WHERE
                            U_NAME = '%s' LIMIT 1""" % u_name
        print(get_user_query)

        try:
            cursor.execute(get_user_query)
            data = cursor.fetchone()
            print((strings.get_success).format(u_name,'USERS'))
            print('U_ID: {0} | U_NAME: {1} | U_AGE: {2} |\
             U_HOME_ADDR: {3} | U_PHONE_NUMBER: {4}'.format(data[0], data[1], data[2], data[3], data[4]))
            db.close()

            return data

        except:
            print((strings.get_failed).format(u_name,'USERS'))
            db.close()

            return 0


    '''
    function: update_user
    description: updates the user
    '''
    def update_user(self, u_id, field, new_value):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        update_user_query = """UPDATE USERS SET %s = '%s' WHERE
                            U_ID = %s""" % (field, new_value, u_id)
        print(update_user_query)
        try:
            cursor.execute(update_user_query)
            db.commit()
            print((strings.update_success).format(u_id,'USERS',new_value))
        except:
            print((strings.update_failed).format(u_id,'USERS',new_value))
            db.rollback()

        db.close()


    '''
    function: delete_user
    description: delete all data of a user given the user_name
    '''
    def delete_user(self,u_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        delete_u_auth_query = """DELETE FROM AUTH WHERE
                                 A_UID = '%s'""" % (u_id)
        delete_u_reminders_query = """DELETE FROM REMINDERS WHERE
                                      R_UID = '%s'""" % (u_id)
        delete_u_locations_query = """DELETE FROM LOCATIONS WHERE
                                      L_UID = '%s'""" % (u_id)
        delete_user_query = """DELETE FROM USERS WHERE
                               U_ID = '%s'""" % (u_id)

        print(delete_u_auth_query)
        print(delete_u_reminders_query)
        print(delete_u_locations_query)
        print(delete_user_query)

        # remove auth
        try:
            cursor.execute(delete_u_auth_query)
            db.commit()
            print((strings.delete_success).format(u_id,'AUTH'))

        except:
            print((strings.delete_failed).format(u_id,'AUTH'))
            db.rollback()

        # remove reminders
        try:
            cursor.execute(delete_u_reminders_query)
            db.commit()
            print((strings.delete_success).format(u_id,'REMINDERS'))

        except:
            print((strings.delete_failed).format(u_id,'REMINDERS'))
            db.rollback()

        # remove locations
        try:
            cursor.execute(delete_u_locations_query)
            db.commit()
            print((strings.delete_success).format(u_id,'LOCATIONS'))

        except:
            print((strings.delete_failed).format(u_id,'LOCATIONS'))
            db.rollback()

        # remove user
        try:
            cursor.execute(delete_user_query)
            db.commit()
            print((strings.delete_success).format(u_id,'USERS'))

        except:
            print((strings.delete_failed).format(u_id,'USERS'))
            db.rollback()

        db.close()

    ## === REMINDERS ===========================================================

    '''
    function: add_reminder
    description: adds a reminder to the reminders table
    '''
    def add_reminder(self,r_name,r_data,r_due,r_usr):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        add_reminder_query = """INSERT INTO REMINDERS (
                                R_NAME, R_DATA, R_DUE, R_UNAME, R_UID ) VALUES (
                                '%s', '%s', '%s', (SELECT U_NAME FROM USERS WHERE
                                U_ID = '%s'), '%s' )""" % (r_name, r_data, r_due, r_usr, r_usr)
        print(add_reminder_query)

        try:
            cursor.execute(add_reminder_query)
            db.commit()
            print((strings.add_success).format('reminder',r_name,'REMINDERS'))

        except:
            print((strings.add_failed).format('reminder',r_name,'REMINDERS'))
            db.rollback()

        db.close()


    '''
    function: get_reminders
    description: fetches reminders given the user_name
    '''
    def get_reminders(self,u_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        get_reminders_query = """SELECT * FROM REMINDERS WHERE
                                 R_UID = '%s'""" % u_id
        print(get_reminders_query)

        try:
            cursor.execute(get_reminders_query)
            rems = cursor.fetchall()
            print((strings.get_success).format(u_id,'REMINDERS'))
            for row in rems:
                print('R_ID: {0} | R_NAME: {1} | R_DATA: {2} | R_DUE: {3}'.format(
                    row[0], row[1], row[2], row[3]))
            db.close()

            return rems

        except:
            print((strings.get_failed).format(u_id,'REMINDERS'))
            db.close()

            return 0

    '''
    function: get_remind
    description: fetches reminder with the given reminder id
    '''
    def get_remind(self, r_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        get_reminders_query = """SELECT * FROM REMINDERS WHERE
                                 R_ID = '%s'""" % r_id
        print(get_reminders_query)

        try:
            cursor.execute(get_reminders_query)
            rem = cursor.fetchone()
            print((strings.get_success).format(r_id,'REMINDERS'))
            print('R_ID: {0} | R_NAME: {1} | R_DATA: {2} | R_DUE: {3}'.format(
                    rem[0], rem[1], rem[2], rem[3]))
            db.close()

            return rem

        except:
            print((strings.get_failed).format(r_id,'REMINDERS'))
            db.close()

            return 0


    '''
    function: update_remind
    description: updates the value of the reminder
    '''
    def update_remind(self, r_id, field, new_value):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        update_rem_query = """UPDATE REMINDERS SET %s = '%s' WHERE
                            R_ID = '%s'""" % (field, new_value, r_id)
        print(update_rem_query)

        try:
            cursor.execute(update_rem_query)
            db.commit()
            print((strings.update_success).format(r_id,'REMINDERS',new_value))

        except:
            print((strings.update_failed).format(r_id,'REMINDERS',new_value))
            db.rollback()

        db.close()


    '''
    function: delete_reminder
    description: deletes the reminder with the given id
    '''
    def delete_reminder(self, r_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        delete_rb_query = """DELETE FROM REMINDERS WHERE
                            R_ID = '%s'""" % r_id
        print(delete_rb_query)

        try:
            cursor.execute(delete_rb_query)
            db.commit()
            print((strings.delete_success).format(r_id,'REMINDERS'))

        except:
            print((strings.delete_failed).format(r_id,'REMINDERS'))
            db.rollback()

        db.close()

    '''
    function: delete_all_reminders
    description: deletes all the reminders associated with the given user id
    '''
    def delete_all_reminders(self, u_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        delete_rb_query = """DELETE FROM REMINDERS WHERE
                             R_UID = '%s'""" % u_id
        print(delete_rb_query)

        try:
            cursor.execute(delete_rb_query)
            db.commit()
            print((strings.delete_success).format('all','REMINDERS for user'))

        except:
            print((strings.delete_failed).format('all','REMINDERS for user'))
            db.rollback()

        db.close()


    ## === LOCATIONS ===========================================================

    '''
    function: add_location
    description: adds a reminder to the reminders table
    '''
    def add_location(self,lon,lat,u_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        dt = str(datetime.now())

        add_location_query = """INSERT INTO LOCATIONS (
                                L_UNAME, L_LON, L_LAT, L_DT, L_UID ) VALUES (
                                (SELECT U_NAME FROM USERS WHERE U_ID = '%s'), '%s', '%s', '%s', '%s')""" % (u_id, lon, lat, dt, u_id)
        print(add_location_query)

        try:
            cursor.execute(add_location_query)
            db.commit()
            print((strings.add_success).format('location',dt,'LOCATIONS'))

        except:
            print((strings.add_failed).format('location',dt,'LOCATIONS'))
            db.rollback()

        db.close()


    '''
    function: get_locations
    description: fetches locations given the user_name
    '''
    def get_locations(self,u_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        get_locations_query = """SELECT * FROM LOCATIONS WHERE L_UID =
                                 '%s' ORDER BY L_ID DESC""" % u_id
        print(get_locations_query)

        try:
            cursor.execute(get_locations_query)
            locs = cursor.fetchall()
            for loc in locs:
                print('L_ID: {0} | L_UNAME: {1} | L_LON: {2} | L_LAT: {3} \
                     | L_DT: {4} | L_UID: {5}'.format(loc[0], loc[1],
                       loc[2], loc[3], loc[4], loc[5]))
            print((strings.get_success).format(u_id,'LOCATIONS'))
            db.close()

            return locs

        except:
            print((strings.get_failed).format(u_id,'LOCATIONS'))
            db.close()

            return 0

    ## === AUTH ================================================================

    '''
    function: get_auth
    description: fetches the auth information associated with the given u_name
    '''
    def get_auth(self, u_name):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        get_auth_query = """SELECT * FROM AUTH WHERE A_NAME = '%s'""" % u_name
        print(get_auth_query)

        try:
            cursor.execute(get_auth_query)
            auths = cursor.fetchone()
            print((strings.get_success).format(u_name,'AUTH'))
            print('A_UID: {0} | A_NAME: {1} | A_PASS: {2} | A_TOKEN: {3}'.format(auths[4], auths[1], auths[2], auths[3]))
            db.close()
            return auths

        except:
            print((strings.get_failed).format(u_name,'AUTH'))
            db.close()

    '''
    function: add_auth
    description: associates the given auth info with the given u_id
    '''
    def add_auth(self, u_id, name, pw, token):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        add_auth_query = """INSERT INTO AUTH (A_UID, A_NAME, A_PASS, A_TOKEN)
                            VALUES ('%s', '%s', '%s', '%s')""" % (u_id, name, pw, token)
        print(add_auth_query)

        try:
            cursor.execute(add_auth_query)
            db.commit()
            print((strings.add_success).format('auth info', u_id,'AUTH'))

        except:
            print((strings.add_failed).format('auth info', u_id,'AUTH'))
            db.rollback()

        db.close()

    '''
    function: update_auth
    description: changes the password or token for the given u_id
    '''
    def update_auth(self, u_id, field, new_val):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()

        update_auth_query = """UPDATE AUTH SET %s = '%s' WHERE A_UID = '%s'""" % (field, new_val, u_id)
        print(update_auth_query)

        try:
            cursor.execute(update_auth_query)
            db.commit()
            print((strings.update_success).format(u_id, field, new_val))
        except:
            print((strings.update_failed).format(u_id, field, new_val))
            db.rollback()

        db.close()
