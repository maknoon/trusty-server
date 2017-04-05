#!/usr/bin/env python

import config
import strings
import json
from trustydb import TrustyDb
from flask import Flask, request, abort
from flask.ext.bcrypt import Bcrypt
from datetime import datetime
app = Flask(__name__)
bcrypt = Bcrypt(app)

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
    usr_id = request.args.get('id')

    # GET - fetches user info from query parameter 'name'
    if request.method == 'GET':
        if usr_id is not None:
            user = trustydb.get_user(usr_id)
        else: abort(400)

        if (user == 0): abort(404)
        else:
            user_json = {"id":user[0],"name":user[1],"age":user[2],
                        "address":user[3],"phone_number":user[4]};
            res_body = json.dumps(user_json, indent=4, separators=(',', ': '))

    # POST - accepts JSON format request body
    elif request.method == 'POST':
        req_body = request.get_json()

        usr_name = req_body["name"]
        usr_age = req_body["age"]
        usr_addr = req_body["address"]
        usr_pnum = req_body["phone_number"]

        # required when a new user is made
        usr_uname = req_body["username"]
        usr_passw = req_body["password"]
        
        insert_id = trustydb.add_user(usr_name,usr_age,usr_addr,usr_pnum)
        if (insert_id == 0): abort(501)
        else:
            password = bcrypt.generate_password_hash(usr_passw)
            if (config.env == 0): password = password.decode('utf-8') # ugh server hack
            trustydb.add_auth(insert_id,usr_uname,password,strings.garbage_token)
            # TODO if the above fails, delete the successfully-inserted user

        res_body = json.dumps(req_body, indent=4, separators=(',', ': '))

    # PUT - updates user info from query parameter 'name'
    elif request.method == 'PUT':
        user = trustydb.get_user(usr_id)

        req_body = request.get_json()

        if (user == 0): abort(404)
        else:
            if "name" in req_body:
                usr_name = req_body["name"]
                # Update name
                trustydb.update_user(user[0], 'U_NAME', usr_name)
            if "age" in req_body:
                usr_age = req_body["age"]
                # Update age
                trustydb.update_user(user[0], 'U_AGE', usr_age)
            if "address" in req_body:
                usr_addr = req_body["address"]
                # Update address
                trustydb.update_user(user[0], 'U_HOME_ADDR', usr_addr)
            if "phone_number" in req_body:
                usr_pnum = req_body["phone_number"]
                # Update address
                trustydb.update_user(user[0], 'U_PHONE_NUMBER', usr_pnum)

        # get user again for the response body
        user = trustydb.get_user(usr_id)
        user_json = {"id":user[0],"name":user[1],"age":user[2],
                    "address":user[3],"phone_number":user[4]}
        res_body = json.dumps(user_json, indent=4, separators=(',', ': '))

    # DELETE - deletes user info from db
    elif request.method == 'DELETE':
        usr_name = (trustydb.get_user(usr_id))[1]
        trustydb.delete_user(usr_id)
        res_body = (strings.deleted).format('user', usr_name)

    return res_body

# =============================================
# AUTH
# =============================================

# handles user login behavior
# NOTE: endpoint accepts Content-Type: application/x-www-form-urlencoded
@app.route('/login', methods=['GET','POST'])
def handle_login():
    res_body = (strings.default_resource).format('Auth')
    trustydb = connect_to_db()

    # GET should show the login form to the user
    if request.method == 'GET':
        res_body = strings.todo

    # user should login and retrieve their id from this endpoint
    elif request.method == 'POST':
        uname = request.form['username']
        passw = request.form['password']

        auth = trustydb.get_auth(uname)
        if (auth == 0): abort(404)
        else:
            # verify the password
            stored = auth[2]
            authenticated = bcrypt.check_password_hash(stored,passw)
            if (authenticated):
                auth_json = {"user_id":auth[0],"username":auth[1],"token":auth[3]}
                res_body = json.dumps(auth_json, indent=4, separators=(',', ': '))
            else:
                print(strings.auth_failed)
                abort(401)
    
    return res_body


# handles user change password behavior
@app.route('/change_password', methods=['PUT'])
def handle_pw_change():
    return strings.todo

# handles device token behavior (resource is tied to AUTH table)
# for now, we do not need authentication to fetch or update tokens
@app.route('/token', methods=['GET','PUT'])
def handle_token():
    res_body = (strings.default_resource).format('Auth')
    trustydb = connect_to_db()
    u_name = request.args.get('username')

    # get the token associated w/ the provided username
    if request.method == 'GET':
        auth = trustydb.get_auth(u_name)
        if (auth == 0): abort(404)
        else:
            auth_json = {"username":auth[1],"token":auth[3]}
            res_body = json.dumps(auth_json, indent=4, separators=(',', ': '))

    # change the token associated w/ the provided username
    elif request.method == 'PUT':
        req_body = request.get_json()
        a_token = req_body["token"]

        u_id = (trustydb.get_auth(u_name))[0] #we only need the U_ID for this operation
        trustydb.update_auth(u_id,'A_TOKEN',a_token)

        auth = trustydb.get_auth(u_name)
        if auth == 0: abort(400)
        else: res_body = (strings.updated).format("token to",auth[3])

    return res_body


# =============================================
# REMINDERS
# =============================================

# handler for the reminders endpoint => REMINDERS
@app.route('/reminders', methods=['GET','POST','DELETE','PUT'])
def handle_reminders():
    res_body = (strings.default_resource).format('Reminders')
    trustydb = connect_to_db()
    usr_id = request.args.get('id')
    usr_name = request.args.get('name')

    # GET - fetches reminders from query parameter 'id'
    if request.method == 'GET':
        reminders = trustydb.get_reminders(usr_id)

        if (reminders == 0): abort(404)
        else:
            reminders_json = []
            for row in reminders:
                reminder = {"reminder_id":row[0],"reminder_name":row[1],
                            "reminder_data":row[2],"reminder_due":row[3].isoformat()}
                reminders_json.append(reminder)

            res_body = json.dumps(reminders_json, indent=4, separators=(',', ': '))

    # POST - accepts JSON format request body
    elif request.method == 'POST':
        req_body = request.get_json()
        r_name = req_body["reminder_name"]
        r_data = req_body["reminder_data"]
        r_due = req_body["reminder_due"]

        if usr_id is None: abort(400)
        trustydb.add_reminder(r_name,r_data,r_due,usr_id)
        res_body = json.dumps(req_body, indent=4, separators=(',', ': '))

    # PUT - updates the reminder information
    elif request.method == 'PUT':
        r_id = request.args.get('id')

        req_body = request.get_json()
        reminder = trustydb.get_remind(r_id);

        if (reminder == 0): abort(404)
        else:
            if "reminder_name" in req_body:
                new_name = req_body["reminder_name"]
                trustydb.update_remind(r_id, 'R_NAME', new_name)

                # Return the new reminder
                reminders_json = []
                reminders = trustydb.get_remind(r_id)
                for row in reminders:
                    reminder = {"reminder_id":row[0],"reminder_name":row[1],
                                "reminder_data":row[2],"reminder_due":row[3].isoformat()}
                    reminders_json.append(reminder)
                res_body = json.dumps(reminders_json, indent=4, separators=(',', ': '))

            if "reminder_data" in req_body:
                new_body = req_body["reminder_data"]
                trustydb.update_remind(r_id, 'R_DATA', new_body)

                # Return the new reminder
                reminders_json = []
                reminders = trustydb.get_remind(r_id)
                for row in reminders:
                    reminder = {"reminder_id":row[0],"reminder_name":row[1],
                                "reminder_data":row[2],"reminder_due":row[3].isoformat()}
                    reminders_json.append(reminder)
                res_body = json.dumps(reminders_json, indent=4, separators=(',', ': '))

            if "reminder_due" in req_body:
                new_body = req_body["reminder_due"]
                trustydb.update_remind(r_id, 'R_DUE', due_dt)

                # Return the new reminder
                reminders_json = []
                reminders = trustydb.get_remind(r_id)
                for row in reminders:
                    reminder = {"reminder_id":row[0],"reminder_name":row[1],
                                "reminder_data":row[2],"reminder_due":row[3].isoformat()}
                    reminders_json.append(reminder)
                res_body = json.dumps(reminders_json, indent=4, separators=(',', ': '))

    # DELETE - deletes user info from db
    elif request.method == 'DELETE':
        r_id = request.args.get('id')

        reminders = trustydb.get_remind(r_id);
        if (reminders == 0): abort(404)
        else:
            trustydb.delete_reminder(r_id);
            res_body = (strings.deleted).format('reminder', '{0}: {1}'.format(r_id,reminders[0][1]))

    return res_body



# =============================================
# LOCATIONS
# =============================================

# handler for the locations endpoint => LOCATIONS
@app.route('/locations', methods=['GET','POST'])
def handle_locations():
    res_body = (strings.default_resource).format('Locations')
    trustydb = connect_to_db()
    usr_id = request.args.get('id')
    latest = request.args.get('latest')

    # catch some bad inputs
    if (latest == '' or usr_id == ''): abort(400)

    # GET - fetches locations from query parameter 'name'
    if request.method == 'GET':
        locations = trustydb.get_locations(usr_id)

        if (locations == 0): abort(404)
        else:
            # fetch all the locations for a user
            locations_json = []
            for loc in locations:
                location = {"longitude":loc[2],"latitude":loc[3],
                            "timestamp":loc[4].isoformat()}
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

        trustydb.add_location(lon,lat,usr_id)
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
