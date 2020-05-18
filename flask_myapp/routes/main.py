from flask import Blueprint, render_template, request, redirect, url_for, session,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests 
import json
import os
import random
import string
import time

#export FLASK_DEBUG=1
#export FLASK_APP=localrun.py
DATABASE_URL=os.environ.get('DATABASE_URL')

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

main = Blueprint('main', __name__)

@main.route('/',methods=['POST','GET'])
def index():
    return "Welcome to CO2 Sensor Server"

@main.route('/summit',methods=['POST','GET'])
def summit():
    cpuserial=request.args.get("serial")
    timestamp=request.args.get("t")
    CO2=float(request.args.get("co2"))
    ts = time.time()
    db.execute(f"""
    INSERT INTO "Received Data" (cpuserial, timestamp, "Received timestamp", "CO2 ppm")
    VALUES ('{cpuserial}', {timestamp}, {ts} ,{CO2});
    COMMIT;
    """)
    return "success"

@main.route('/search',methods=['POST','GET'])
def search():
    if (request.method == 'POST'):
        cpuserial=request.args.get("serial")
        if (cpuserial==None):
            cpuserial=request.form.get("serial")
        if (cpuserial==None or cpuserial==""):
            return "ERROR getting Serial!"
        fet=db.execute(f"""
        SELECT timestamp,"CO2 ppm" FROM "Received Data" WHERE cpuserial='{cpuserial}'
        """).fetchall()
        csv="timestamp,CO2 ppm"
        for i in fet:
            csv=csv+"<br>"+str(i[0])+","+str(i[1])
            print(i)
        return csv
    else:
        return """
            <label for="site-search">Search the CO2 sensor:</label>
            <form action="/search" method="post">
            <input type="search" id="site-search" name="serial" aria-label="Search through Database">
            <button type="summit">Search</button>
            </form>
            """