# Imports
###########################################################

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from dateutil.parser import parse

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
def precip():
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database

    late_date = session.query(Measure.date).order_by(Measure.date.desc()).first()

    #Get the string out of the result object
    late_date_str = late_date[0]

    # Converting the string in late_date to a datetime object
    late_date_dt = parse(late_date_str)

    #The date 1 year prior to the last day in the dataset 
    early_date_dt = late_date_dt - dt.timedelta(days=365)

    #Store the early date in a string for later
    early_date_str = early_date_dt.strftime("%Y-%m-%d")

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measure.date, Measure.prcp).\
    filter(Measure.date > early_date_str).filter(Measure.date <= late_date_str).all()

    session.close()

    results_dict = {}

    # Building a dictionary, where key is date and value is a list of precipitations
    for row in results:
        if row[0] in results_dict:
            results_dict[row[0]].append(row[1])
        else:
            results_dict[row[0]] = [row[1]] 
        

    return jsonify(results_dict)
    
@app.route("/api/v1.0/stations")
def stations(): 
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    results_list = list(np.ravel(results))

    return jsonify(results_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database

    late_date = session.query(Measure.date).order_by(Measure.date.desc()).first()

    #Get the string out of the result object
    late_date_str = late_date[0]

    # Converting the string in late_date to a datetime object
    late_date_dt = parse(late_date_str)

    #The date 1 year prior to the last day in the dataset 
    early_date_dt = late_date_dt - dt.timedelta(days=365)

    #Store the early date in a string for later
    early_date_str = early_date_dt.strftime("%Y-%m-%d")

    results = session.query(Measure.date, Measure.tobs).\
        filter(Measure.station == 'USC00519281').\
        filter(Measure.date > early_date_str).\
        filter(Measure.date <= late_date_str).all()

    session.close()

    temp_results = []

    for row in results:
        temp_results.append(row[1])

    return jsonify(temp_results)




@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Fetch the temperatures for every day after the start date and before end date.



    session = Session(engine)

    
    #Get the string out of the result object
    late_date_str = end


    #canonicalized = start.replace("/", "-")

    results = session.query(Measure.tobs).\
        filter(Measure.station == 'USC00519281').\
        filter(Measure.date >= start).\
        filter(Measure.date <= late_date_str).all()

    session.close()

    results_list = list(np.ravel(results))

    min_temp = min(results_list)
    avg_temp = sum(results_list)/len(results_list)
    max_temp = max(results_list)

    dict = {"Minimum Temp":min_temp, "Average Temp":avg_temp, "Maximum Temp":max_temp}

    return jsonify(dict)



@app.route("/api/v1.0/<start>")
def start(start):
    # Fetch the temperatures for every day after the start date.



    session = Session(engine)

    # Late date is again the first row in a sorted descending list of dates
    late_date = session.query(Measure.date).order_by(Measure.date.desc()).first()

    #Get the string out of the result object
    late_date_str = late_date[0]


    #canonicalized = start.replace("/", "-")

    results = session.query(Measure.tobs).\
        filter(Measure.station == 'USC00519281').\
        filter(Measure.date >= start).\
        filter(Measure.date <= late_date_str).all()

    session.close()

    results_list = list(np.ravel(results))

    min_temp = min(results_list)
    avg_temp = sum(results_list)/len(results_list)
    max_temp = max(results_list)

    dict = {"Minimum Temp":min_temp, "Average Temp":avg_temp, "Maximum Temp":max_temp}

    return jsonify(dict)



@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>tobs</a><br/>"
        
    )


if __name__ == "__main__":
    app.run(debug=True)
