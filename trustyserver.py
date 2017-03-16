#!/usr/bin/env python

import config
import strings
import json
from trustydb import TrustyDb
from flask import Flask, request, abort
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
# USERS
# =============================================

# handler for the users endpoint => USERS
@app.route('/users', methods=['GET','POST','PUT','DELETE'])
def handle_users():
    res_body = (strings.default_resource).format('Users')
    trustydb = connect_to_db()
    usr_name = request.args.get('name')

    # GET - fetches user info from query parameter 'name'
    if request.method == 'GET':
        user = trustydb.get_user(usr_name)

        if (user == 0): abort(404)
        else:
            user_json = {"name":user[1],"age":user[2],"address":user[3]};
            res_body = json.dumps(user_json, indent=4, separators=(',', ': '))

    # POST - accepts JSON format request body
    elif request.method == 'POST':
        req_body = request.get_json()
        usr_name = req_body["name"]
        usr_age = req_body["age"]
        usr_addr = req_body["address"]

        trustydb.add_user(usr_name,usr_age,usr_addr)
        res_body = json.dumps(req_body, indent=4, separators=(',', ': '))

    # PUT - updates user info from query parameter 'name'
    elif request.method == 'PUT':
        res_body = 'UPDATING {}'.format(usr_name)

    # DELETE - deletes user info from db
    elif request.method == 'DELETE':
        trustydb.delete_user(usr_name)
        res_body = (strings.deleted).format('user', usr_name)

    return res_body



# =============================================
# REMINDERS
# =============================================

# handler for the reminders endpoint => REMINDERS
@app.route('/reminders', methods=['GET','POST','DELETE'])
def handle_reminders():
    res_body = (strings.default_resource).format('Reminders')
    trustydb = connect_to_db()
    usr_name = request.args.get('name')

    # GET - fetches reminders from query parameter 'name'
    if request.method == 'GET':
        reminders = trustydb.get_reminders(usr_name)

        if (reminders == 0): abort(404)
        else:
            reminders_json = []
            for row in reminders:
                reminder = {"reminder_name":row[1],"reminder_data":row[2]}
                reminders_json.append(reminder)

            res_body = json.dumps(reminders_json, indent=4, separators=(',', ': '))

    # POST - accepts JSON format request body
    elif request.method == 'POST':
        req_body = request.get_json()
        r_name = req_body["reminder_name"]
        r_data = req_body["reminder_data"]

        trustydb.add_reminder(r_name,r_data,usr_name)
        res_body = json.dumps(req_body, indent=4, separators=(',', ': '))

    # DELETE - deletes user info from db
    elif request.method == 'DELETE':
        res_body = strings.todo

    return res_body



# =============================================
# LOCATIONS
# =============================================

# handler for the locations endpoint => LOCATIONS
@app.route('/locations', methods=['GET','POST'])
def handle_locations():
    res_body = (strings.default_resource).format('Locations')
    trustydb = connect_to_db()
    usr_name = request.args.get('name')
    latest = request.args.get('latest')

    # catch some bad inputs
    if (latest == '' or usr_name == ''): abort(400)

    # GET - fetches locations from query parameter 'name'
    if request.method == 'GET':
        locations = trustydb.get_locations(usr_name)

        if (locations == 0): abort(404)
        else:
            # fetch all the locations for a user
            locations_json = []
            for loc in locations:
                dt = loc[4].isoformat()
                location = {"longitude":loc[2],"latitude":loc[3],"timestamp":dt}
                locations_json.append(location)

            # if latest is specified, use only latest x locations
            if latest is None: latest = len(locations_json)
            else: latest = int(latest)
            
            res_body = json.dumps(locations_json[0:latest], indent=4,
                separators=(',', ': '))

    # POST - accepts JSON format request body
    elif request.method == 'POST':
        req_body = request.get_json()
        lon = req_body["longitude"]
        lat = req_body["latitude"]

        trustydb.add_location(lon,lat,usr_name)
        res_body = json.dumps(req_body, indent=4, separators=(',', ': '))

    return res_body



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

