from flask import Flask, jsonify
from sqlquery import read
from sqlquery import final_entry


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
    query = 'SELECT * FROM station'
    result = read(query)
    return jsonify(dict(result))

# temperature observations page
@app.route('/api/v1.0/tobs')
def tobs():
    from sqlquery import get_tobs
    temp_obs = get_tobs(final_entry.date)
    return jsonify(dict(temp_obs))

# calculates min, avg, max temp between start and end date
# if no end date, calculates for all dates >= start date
@app.route('/api/v1.0/<start>')
def start_dates(start):
    from sqlquery import calc_temps
    val = calc_temps(start, final_entry.date)
    print(f"LOG {final_entry.date}")
    summary = {"min" : val[0], 
        "avg" : val[1], 
        "max" : val[2]
    }
    return jsonify(summary)


@app.route('/api/v1.0/<start>/<end>')
def dates(start, end):
    from sqlquery import calc_temps
    val = calc_temps(start, end)
    print(f"LOG {val[0]}")
    print(f"LOG {val[1]}")
    print(f"LOG {val[2]}")

    summary = {"min" : val[0], 
        "avg" : val[1], 
        "max" : val[2]
    }
    return jsonify(summary)

if __name__=="__main__":
    app.run(debug=True)
