# import dependencies
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
import datetime as dt

from pprint import pprint


# create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect existing database
Base = automap_base()
Base.prepare(engine, reflect=True)

# table references
Measurement = Base.classes.measurement
Station = Base.classes.station

# session link from Python to db
session = Session(engine)

# queries final entry
final_entry = engine.execute("SELECT * FROM measurement ORDER BY date DESC").first()


# read function
def read(query):
    return engine.execute(query).fetchall()

# queries all temperature observations one year before input date
def get_tobs(input_date):
    previous_yr = dt.datetime.strptime(input_date, '%Y-%m-%d') - dt.timedelta(days=365)
    qry = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= previous_yr).statement
    result = read(qry)
    return result

# calculate max, avg, min temperature observations between start_date and end_date
# inputs must be strings in the format %Y-%m-%d
def calc_temps(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).first()
