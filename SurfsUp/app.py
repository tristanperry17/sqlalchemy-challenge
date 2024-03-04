# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
app = Flask(__name__)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
measure = Base.classes.measurement
stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)




#################################################
# Flask Routes
#################################################
#Homepage
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Enter start date to get min, max, avg temps from that date onward- Try /api/v1.0/2016-08-23 to start from August 23, 2016<br/>"
        f"/api/v1.0/<start><br/>"
        f"To view min, max, and avg temps in a range of dates, enter start date then end date- Try /api/v1.0/2016-08-23/2017-08-23 to start from August 23, 2016<br/>"
        f"and end August 23, 2017<br/>"
        f"/api/v1.0/<start>/<end>"
    )
#Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to target prcp in last year
    results = session.query(measure.station, measure.date, measure.prcp).\
    filter(measure.date >= '2016-08-23').\
    order_by(measure.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    all_precip = []
    for station, date, prcp in results:
        precip_dict = {}
        precip_dict["station"] = station
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

#List stations
@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(measure.station, func.count(measure.station)).group_by(measure.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

#Temps for most active station
@app.route("/api/v1.0/tobs")
def temperatures():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temperatures for station in question
    results = session.query(measure.station, measure.date, measure.tobs).\
    filter((measure.station == 'USC00519281'),(measure.date >= '2016-08-23')).\
    order_by(measure.date).all()

    session.close()

    # Convert list of tuples into normal list
    temps = list(np.ravel(results))

    return jsonify(temps)

#Temp stats from a start date
@app.route("/api/v1.0/<start>", methods=['GET'])
def temps(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for min, max, avg temps filtered to start at <start>
    results = session.query(measure.date, measure.tobs, func.min(measure.tobs), func.max(measure.tobs, func.avg(measure.tobs))).\
    filter((measure.date >= start)).\
    order_by(measure.tobs).all()
    

    session.close()

    # Convert list of tuples into normal list
    tempstats = list(np.ravel(results))

    return jsonify(tempstats)

#Temp stats from range
@app.route("/api/v1.0/<start>/<end>", methods=['GET'])
def temprange(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for min, max, avg temps filtered to start at <start>, end at <end>
    results = session.query(measure.date, measure.tobs, func.min(measure.tobs), func.max(measure.tobs, func.avg(measure.tobs))).\
    filter((measure.date >= start), (measure.date <= end)).\
    order_by(measure.tobs).all()
    

    session.close()

    # Convert list of tuples into normal list
    trs = list(np.ravel(results))

    return jsonify(trs)






if __name__ == '__main__':
    app.run(debug=True)

