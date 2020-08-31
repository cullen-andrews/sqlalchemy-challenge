# Imports
###########################################################

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify



# Database Setup
###########################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table

Measure = Base.classes.measurement

Station = Base.classes.station



# Flask Setup
##############################################################

app = Flask(__name__)



# Flask Routes
##############################################################


@app.route("/api/v1.0/precipitation")



@app.route("/api/v1.0/stations")


@app.route("/api/v1.0/tobs")



# # 3. Define what to do when a user hits the index route
# @app.route("/")
# def home():
#     print("Server received a request for the 'Home' page...")
#     return "All available routes will be on this page"


# 4. Define what to do when a user hits the /about route
# @app.route("/about")
# def about():
#     print("Server received request for 'About' page...")
#     return "Welcome to my 'About' page!"


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>tobs</a><br/>"
        # f"<a href='/api/v1.0/<start>'><start></a><br/>"
        # f"<a href='/api/v1.0/<start>/<end>'><start>/<end></a><br/>"
    )




if __name__ == "__main__":
    app.run(debug=True)
