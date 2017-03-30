from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

from app import endpoints
