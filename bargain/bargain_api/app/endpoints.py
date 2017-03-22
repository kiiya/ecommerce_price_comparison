"""API endpoints."""
from app import API
from flask import jsonify, Response, render_template
from app import mongo
from bson import json_util


@API.route('/')
def index():
    """Default endpoint."""
    products = mongo.db.jumia.find().limit(20)
    return render_template('index.html', products=products)


