import numpy as np
import pandas as pd

#06-Ins_Jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite", echo=False)

# reflect an existing database into a new model (Ins_Reflection.ipynb)
Base = automap_base()
#reflect tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

#List all routes that are available. (04-Ins_First_Steps_with_Flask)(08-Ins_Variable_Rule)(10-Ins_Flask_with_ORM)
@app.route("/")
def welcome():
    return (
        f"Hawaii Climate API<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>" 
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )
    
    #Convert the query results to a dictionary using date as the key and prcp as the value. (10-Ins_Flask_with_ORM)
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session=Session(engine)
    
#Return a list of all precipitation"""
        
results = session.query(Measurement.date, Measurement.prcp).\
order_by(Measurement.date).all()
        
session.close()

all_precip = []

    for date,prcp in results
    precip_dict = {}
    precip_dict = ["date"] = prcp
    all_precip.append(precip_dict)

return jsonify(all_precip)

@app.route("/api/v1.0/station")
def stations():
    session = Session(engine)
    
    active_stations_totals = session.query(Measurement.station, func.count(Measurement.station)).\
                    group_by(Measurement.station).\
                    order_by(func.count(Measurement.station).desc()).all()
    
    session.close()
    
return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    Station_281 = session.query(Measurement.date, Measurement.tobs).\
filter(Measurement.station == "USC00519281").\
filter(func.strftime("%Y-%m-%d", Measurement.date) >= '2016-08-23').all()

session.close()

all_tobs = []

    for date, tobs in results
    tobs_dict = {}
    tobs_dict[date] = tobs
    all_tobs.append(tobs_dict)

return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def startdate(start)

session = Session(engine)

low_temp = session.query(func.min(Measurement.tobs)).\
filter(Measurement.station == "USC00519281").\
group_by(Measurement.station).all()
print(f"Lowest temp is {low_temp}")

high_temp = session.query(func.max(Measurement.tobs)).\
filter(Measurement.station == "USC00519281").\
group_by(Measurement.station).all()
print(f"Highest temp is {high_temp}")

avg_temp = session.query(func.avg(Measurement.tobs)).\
filter(Measurement.station == "USC00519281").\
group_by(Measurement.station).all()
print(f"Average temp is {avg_temp}")

session.close()

if __name__ == '__main__':
    app.run(debug=True)
