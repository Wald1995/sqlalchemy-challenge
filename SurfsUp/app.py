# Import the dependencies.
import os
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
db_path = r"SurfsUp/Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{db_path}")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables 
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        "Hawaii API<br/>"
        "Available Routes:<br/>"
        "<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        "<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        "<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        "/api/v1.0/<start_date> (replace start_date in yyyy-mm-dd format)<br/>"
        "/api/v1.0/<start_date>/<end_date> (replace start_date and end_date in yyyy-mm-dd format)"
    )

@app.route("/api/v1.0/precipitation")
def get_precipitation():
    results = session.query(
        measurement.date, func.max(measurement.prcp)
    ).filter(measurement.date >= "2016-08-23").group_by(measurement.date).all()

    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {"date": date, "prcp": prcp}
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def get_stations():
    results = session.query(station.station, station.name).all()

    station_names = list(np.ravel(results))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def get_tobs():
    results = session.query(
        measurement.tobs, measurement.date
    ).filter(measurement.station == "USC00519281", measurement.date >= "2016-08-18").all()

    temp = list(np.ravel(results))
    return jsonify(temp)

@app.route("/api/v1.0/<start_date>")
def get_start_data(start_date):
    
    results = session.query(
        func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)
    ).filter(measurement.date >= start_date).all()

    start_data = list(np.ravel(results))
    return jsonify(start_data)

@app.route("/api/v1.0/<start_date>/<end_date>")
def get_start_end_data(start_date, end_date):
    results = session.query(
        func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)
    ).filter(measurement.date.between(start_date, end_date)).all()

    end_data = list(np.ravel(results))
    return jsonify(end_data)

if __name__ == "__main__":
    app.run(debug=True)
