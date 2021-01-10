from flask import Flask, request, jsonify
from datetime import datetime as dt
from pysolar.solar import *
import datetime
import pytz
from timezonefinder import TimezoneFinder
import validation


app = Flask(__name__)


@app.errorhandler(validation.InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/detect_glare', methods=['POST'])
def detect_glare():
    # Read requests parameters (JSON)
    data = request.get_json()
    validation.validate_request(data)
    lat = data['lat']
    lon = data['lon']
    # unix time or amount of time in seconds that has elapsed since January 1st, 1970 (00:00:00 UTC)
    epoch = data['epoch']
    orientation = data['orientation']
    # finding the date based on epoch in UTC timezone
    date = dt.fromtimestamp(epoch, datetime.timezone.utc)
    tf = TimezoneFinder()
    # finding timezone of object based on latitude and longitude
    tf = tf.timezone_at(lng=lon, lat=lat)
    # converting time from UTC to new timezone
    time = date.astimezone(pytz.timezone(tf))
    solar_altitude = get_altitude(lat, lon, time)
    solar_azimuth = get_azimuth(lat, lon, time)
    if orientation < 0:
        car_azimuth = orientation + 360
    else:
        car_azimuth = orientation

    if abs(solar_azimuth - car_azimuth) < 30 and 0 < solar_altitude < 45:
        glare = True
    else:
        glare = False

    response = {'glare': str(glare)}
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
