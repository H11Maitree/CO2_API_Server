from flask import Blueprint, render_template, request, redirect, url_for, session,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests 
import json
import os
import random
import string

#export FLASK_DEBUG=1
#export FLASK_APP=localrun.py
DATABASE_URL=os.environ.get('DATABASE_URL')

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

main = Blueprint('main', __name__)

@main.route('/',methods=['POST','GET'])
def index():
    return "Welcome to CO2 Sensor Server"
