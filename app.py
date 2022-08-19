from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}}) #currently set for ALL ROUTES and origin is set to all the any IP @internet