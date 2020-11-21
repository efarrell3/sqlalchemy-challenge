# Dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import flask, jsonify

# Database Setup
engine = create_engine("sqlite://Resources/hawaii.sqlite")

#reflect existing database into a new model
Base = automap_base()

Base.prepare(engine, reflect=True)

#Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask Setup
app = Flask(_name_)

#Flask Routes
@app.route("/")
def welcome():
    """List all routes that are available"""
    return(
        f"Available Routes:<br/>"
        f"<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature from One Year Prior to Last Data Point: /api/v1.0/tobs<br/>"
        f"<br/>"
        f"Min, Max, and Avg Temperature from Given Start Date: /api/v1.0/min_max_avg/&lt;start date&gt;<br/>"
        f"Min, Max, and Avg Temperature from Given Start and End Dates: /api/v1.0/min_max_avg/&lt;start date&gt;/&lt;end date&gt;"
    )


### PRECIPITATION
@app.route('/api/v1.0/precipitation')
def precipitation():
    # create session link
    session = Session(engine)
    # query for dates and precipitation values
    sel = [Measurement.date, Measurement.prcp]
    queryres = session.query(*sel).all()
    session.close()

    # convert to list of dictionaries to jsonify
    precipitation = []
    for date, prcp in queryres:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)


### STATIONS
@app.route('/api/v1.0/stations')
def stations():
    # create session link
    session = Session(engine)
    # query all stations
    sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    queryres = session.query(*sel).all()
    session.close()

      # convert to list of dictionaries to jsonify
    stations = []
    for station,name,lat,lon,el in queryres:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Latitude"] = lat
        station_dict["Longitude"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)


### TOBS
@app.route('/api/v1.0/tobs')
def tobs():
    # create session link
    session = Session(engine)
    # get last date in dataset and date from year prior
    lateststr = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latestdate = dt.datetime.strptime(lateststr, '%Y-%m-%d')
    querydate = dt.date(latestdate.year-1, latestdate.month, latestday)
    # query for dates and temps
    sel = [Measurement.date, Measurement.tobs]
    queryres = session.query(*sel).filter(Measurement.date >= querydate).all()
    session.close()

     # convert to list of dictionaries to jsonify 
    tobsall = []
    for date, tobs in queryres:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobsall.append(tobs_dict)

    return jsonify(tobsall)


### START DATE
@app.route('/api/v1.0/min_max_avg/<start>')
def start(start):
    # create session link
    session = Session(engine)
    #get start date
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    # query min, avg, and max temp filtered by start date
    queryres = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >=start_date).all()
    session.close()

    # convert to list of dictionaries to jsonify 
    tobsall = []
    for min,avg,max in queryres:
        tobs_dict = {}
        tobs_dict["Start Date"] = start_date
        tobs_dict["Minimum"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Maximum"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)


### END DATE
@app.route('/api/v1.0/min_max_avg/<start>/<end>')
def get_start_stop(start,end):
    # create session link
    session = Session(engine)
    #get start and end dates
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    # query min, avg, and max temp filtered by start date to end date
    queryres = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()

   # convert to list of dictionaries to jsonify 
    tobsall = []
    for min,avg,max in queryres:
        tobs_dict = {}
        tobs_dict["Start Date"] = start_date
        tobs_dict["End Date"] = end_date
        tobs_dict["Minimum"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Maximum"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)

#run the app
if _name_ == '_main_':
    app.run(debug=True)



    
