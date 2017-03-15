#!/usr/bin/env python

import config
import strings
import json
from trustydb import TrustyDb
from flask import Flask, request
from datetime import datetime
app = Flask(__name__)



# =============================================
# HOME
# =============================================

# main page
@app.route('/')
def home():
    return strings.greeting



# =============================================
# DEBUG ENDPOINTS
# =============================================

# reset the database
@app.route('/reset')
def reset():
    trustydb = connect_to_db()
    trustydb.reset_db()

    return strings.reset


# test return a string as response from server
@app.route('/test/<input_str>')
def test(input_str):
    return input_str


# return the reversed string
@app.route('/reverse/<input_str>')
def reverse(input_str):
    return input_str[::-1]



# =============================================
# USERS ENDPOINTS
# =============================================

# insert a new user into the users table
@app.route('/users/add', methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        content = request.get_json()
        usr_name = content["name"]
        usr_age = content["age"]
        usr_addr = content["address"]

        trustydb = connect_to_db()
        trustydb.add_user(usr_name,usr_age,usr_addr)
        print((strings.added_usr).format(usr_name))

        return json.dumps(content, indent=4, separators=(',', ': '))

    else:
        return strings.use_post


# get a user's information given name of the user
@app.route('/users/get/<usr_name>')
def get_user(usr_name):
    trustydb = connect_to_db()
    user = trustydb.get_user(usr_name)

    if (user == 0):
        return strings.user_get_failed
    else:
        user_json = {"name":user[1],"age":user[2],"address":user[3]};
        return json.dumps(user_json, indent=4, separators=(',', ': '))



# =============================================
# REMINDERS ENDPOINTS
# =============================================

# insert a reminder into the reminders table
@app.route('/reminders/add/<usr_name>', methods=['GET', 'POST'])
def add_reminder(usr_name):
    if request.method == 'POST':
        content = request.get_json()
        r_name = content["reminder_name"]
        r_data = content["reminder_data"]

        trustydb = connect_to_db()
        trustydb.add_reminder(r_name,r_data,usr_name)

        return json.dumps(content, indent=4, separators=(',', ': '))

    else:
        return strings.use_post


# get a list of reminders given a user
@app.route('/reminders/get/<usr_name>')
def get_reminders(usr_name):
    trustydb = connect_to_db()
    reminders = trustydb.get_reminders(usr_name)

    if (reminders == 0):
        return strings.reminders_get_failed
    else:
        reminders_json = []
        for row in reminders:
            reminder = {"reminder_name":row[1],"reminder_data":row[2]}
            reminders_json.append(reminder)

        return json.dumps(reminders_json, indent=4, separators=(',', ': '))



# =============================================
# LOCATIONS ENDPOINTS
# =============================================

# insert a location into the location table
@app.route('/locations/add/<usr_name>', methods=['GET', 'POST'])
def add_location(usr_name):
    if request.method == 'POST':
        content = request.get_json()
        lon = content["longitude"]
        lat = content["latitude"]

        trustydb = connect_to_db()
        trustydb.add_location(lon,lat,usr_name)

        return json.dumps(content, indent=4, separators=(',', ': '))

    else:
        return strings.use_post


# get a list of locations given a user
@app.route('/locations/get/<usr_name>')
def get_locations(usr_name):
    trustydb = connect_to_db()
    locations = trustydb.get_locations(usr_name)

    if (locations == 0):
        return strings.locations_get_failed
    else:
        locations_json = []
        for loc in locations:
            dt = loc[4].isoformat()
            location = {"longitude":loc[2],"latitude":loc[3],"timestamp":dt}
            locations_json.append(location)

        return json.dumps(locations_json, indent=4, separators=(',', ': '))



# =============================================
# etc
# =============================================

# HACK.. shouldn't have to do this
def connect_to_db():
    if (config.env == 0): return trustydb
    else:
        print('Connecting to db...{}'.format(config.dbname))
        return TrustyDb(host=config.host,
                        user=config.dbusr,
                        pw=config.dbpwd,
                        db=config.dbname)


if __name__ == '__main__':  
    print('Connecting to db...{}'.format(config.dbname))
    trustydb = TrustyDb(host=config.host,
                        user=config.dbusr,
                        pw=config.dbpwd,
                        db=config.dbname)
    app.run()

