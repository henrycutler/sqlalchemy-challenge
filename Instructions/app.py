import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Instructions/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation"""
    # Query all precipitation
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= "2016-08-23").\
        all()

    session.close()

  # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_precipitation.append(prcp_dict)

    return jsonify(all_precipitation)

# ---------------------------------------------------

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(station.station).\
        order_by(station.station).all()

    session.close()

 
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# ---------------------------------------------------

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs"""
    # Query all tobs
    results = session.query(measurement.date, measurement.tobs, measurement.prcp).\
        filter(measurement.date >= "2016-08-23").\
        filter(measurement.station == "USC00519281").\
        order_by(measurement.date).all()

    session.close()

  # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for date, prcp, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["prcp"] = prcp
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

# ---------------------------------------------------

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    start_date = str(start)

    """Return a list of all tobs"""
    # Query all tobs equal to and after start date
    results = session.query(func.min(measurement.tobs), 
                                         func.max(measurement.tobs), 
                                         func.avg(measurement.tobs)).\
                                         filter(measurement.date >= start_date).\
                                         order_by(measurement.date).all()
    session.close()

  # Create a dictionary from the row data 
  
    tobs_stats = {}
    tobs_stats['TMIN'] = results[0][0]
    tobs_stats['TMAX'] = results[0][1]
    tobs_stats['TAVG'] = results[0][2]

    return jsonify(tobs_stats)


# ---------------------------------------------------

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    start_date = str(start)
    end_date = str(end)

    """Return a list of all tobs"""
    # Query all tobs equal to and after start date and less than equal to end date
    results = session.query(func.min(measurement.tobs), 
                                         func.max(measurement.tobs), 
                                         func.avg(measurement.tobs)).\
                                         filter(measurement.date >= start_date).\
                                         filter(measurement.date <= end_date).\
                                         order_by(measurement.date).all()
    session.close()

  # Create a dictionary from the row data 
    
    tobs_stats = {}
    tobs_stats['TMIN'] = results[0][0]
    tobs_stats['TMAX'] = results[0][1]
    tobs_stats['TAVG'] = results[0][2]

    return jsonify(tobs_stats)



if __name__ == "__main__":
    app.run(debug=True)
