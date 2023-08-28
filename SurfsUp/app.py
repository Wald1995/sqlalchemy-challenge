# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start-date<br/>"
        f"/api/v1.0/start-date/end-date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list"""
    results = (session.query(measurement.date, func.max(measurement.prcp)).filter(measurement.date>='2016-08-23').group_by(measurement.date).all())
    results

    session.close()

    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list"""
    results = session.query(station.station, station.name).all()

    session.close()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list"""
    results = session.query(measurement.tobs, measurement.date).filter(measurement.station=='USC00519281', measurement.date >= '2016-08-18').all()

    session.close()

    # Convert list of tuples into normal list
    temp = list(np.ravel(results))

    return jsonify(temp)

@app.route("/api/v1.0/<start>")
def start(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list"""
    results = session.query(measurement.date,func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    strt = list(np.ravel(results))

    return jsonify(strt)

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list"""
    results = session.query(measurement.date,func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date.between(start, end)).all()

    session.close()

    # Convert list of tuples into normal list
    endd = list(np.ravel(results))

    return jsonify(endd)

if __name__ == '__main__':
    app.run(debug=True)