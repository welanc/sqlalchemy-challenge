from flask import Flask, jsonify

# Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import numpy as np
import pandas as pd
import datetime as dt

# Create an engine for the hawaii.sqlite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create variables to hold classes
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a database session object
session = Session(engine)



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date 1 year ago from the last data point in the database
    last_row = session.query(Measurement).order_by(Measurement.id.desc()).first()
    last_row.__dict__
    last_date = dt.datetime.strptime(last_row.date, '%Y-%m-%d')
    last_year = last_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    year_data = session.query(Measurement.date,func.max(Measurement.prcp)).\
        filter(Measurement.date >= last_year).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()
    
    # Convert data into a dictionary
    daily_data = dict(year_data)

    # Close session for next query
    session.close()

    return jsonify(daily_data)


@app.route("/api/v1.0/stations")
def stations(): 
    # Get Station names and return as a list
    stations_results = session.query(Station.name).all()
    stations_list = list(np.ravel(stations_results))
 
    # Close session for next query
    session.close()
 
    return jsonify(stations_list)  


@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date 1 year ago from the last data point in the database
    last_row = session.query(Measurement).order_by(Measurement.id.desc()).first()
    last_row.__dict__
    last_date = dt.datetime.strptime(last_row.date, '%Y-%m-%d')
    last_year = last_date - dt.timedelta(days=365)

    # List of columns for sqlite to query
    sel = [Measurement.date, Measurement.tobs]

    # Query sqlite database for the most active station over the last year of data
    most_active_st_year = session.query(Measurement.tobs).\
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date >= last_year).\
    order_by(Measurement.date).all()

    # Turn query into list
    most_active_list = list(np.ravel(most_active_st_year))

    # Close session for next query
    session.close()

    return jsonify(most_active_list)


@app.route("/api/v1.0/<start>")
def temperatures_start(start):
    # List to iterate for session query
    temp_data = [
        func.min(Measurement.tobs), 
        func.max(Measurement.tobs), 
        func.avg(Measurement.tobs)
    ]

    # Query sqlite database for the most active station over the last year of data
    temp_stats = session.query(*temp_data).\
    filter(Measurement.date >= start).all()
    
    # Turn query into list
    temp_list = list(np.ravel(temp_stats))

    # Close session for next query
    session.close()

    return jsonify(temp_stats)


@app.route("/api/v1.0/<start>/<end>")
def temperatures_start_end(start,end):
    # List to iterate for session query
    temp_data = [
        func.min(Measurement.tobs), 
        func.max(Measurement.tobs), 
        func.avg(Measurement.tobs)
    ]

    # Query sqlite database for the most active station over the last year of data    
    temp_stats = session.query(*temp_data).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    
    # Turn query into list
    temp_list = list(np.ravel(temp_stats))

    # Close session for next query
    session.close()

    return jsonify(temp_stats)


if __name__ == "__main__":
    app.run(debug=True)
