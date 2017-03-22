"""Initialize and setup api object."""
from flask import Flask
from flask_pymongo import PyMongo

API = Flask(__name__)
API.config.from_object("config.DevConfig")
mongo = PyMongo(API)

from app import endpoints, models