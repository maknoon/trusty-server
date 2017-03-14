#!/usr/bin/env python

import config
from trustydb import TrustyDb
from flask import Flask
app = Flask(__name__)


# main page
@app.route('/')
def home():
    return 'Hello Trusty User!'


# test return a string
@app.route('/test/<input_str>')
def test(input_str):
    return input_str


# return the reversed string
@app.route('/reverse/<input_str>')
def reverse(input_str):
    return input_str[::-1]


# insert a reminder into the reminders table
@app.route('/reminders/add/<input_str>')
def add_reminder(input_str):
    print('Connecting to db... {}'.format(config.dbname))
    trustydb = TrustyDb(host='localhost',
                        user=config.dbusr,
                        pw=config.dbpwd,
                        db=config.dbname)

    trustydb.add_reminder('Fun activity','Smoke some cheeky hookah with Jesus',input_str)

    return 'Reminder added!'



if __name__ == '__main__':    
    app.run()
