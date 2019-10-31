from flask import Flask, jsonify
from sqlquery import read, calc_temps, get_tobs, final_entry

# create instance of Flask
app = Flask(__name__)

# home page
@app.route('/')
def home():
    routes = '''
    The following routes are available: \n
    /api/v1.0/precipitation \n
    /api/v1.0/stations \n
    /api/v1.0/tobs \n
    /api/v1.0/<start>/<end>
    '''
    return routes

# precipitation page
@app.route('/api/v1.0/precipitation')
def precipitation():
    query = 'SELECT date, prcp FROM measurement'
    result = read(query)
    return jsonify(dict(result))

# stations page
@app.route('/api/v1.0/stations')
def stations():
    query = 'SELECT station.station, station.name FROM station'
    result = read(query)
    return jsonify(dict(result))

# temperature observations page
@app.route('/api/v1.0/tobs')
def tobs():
    temp_obs = get_tobs(final_entry.date)
    return jsonify(dict(temp_obs))

# calculates min, avg, max temp between start and end date
# if no end date, calculates for all dates >= start date
@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def dates(start, end=final_entry.date):
    val = calc_temps(start, end)
    summary = {"min" : val[0], 
        "avg" : val[1], 
        "max" : val[2]
    }
    return jsonify(summary)

if __name__=="__main__":
    app.run(debug=True)
