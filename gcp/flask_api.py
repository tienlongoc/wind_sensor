from flask import Flask, request, render_template
import mysql.connector
from datetime import datetime
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="wind_sensor",
  passwd="password",
  database="wind_sensor_db"
)
mycursor = mydb.cursor(buffered=True)

app = Flask(__name__)

def validate_date(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y%m%d-%H:%M").strftime('%Y%m%d-%H:%M'):
            raise ValueError
        return True
    except ValueError:
        return False

@app.route("/", methods=['GET'])
def home():
    day = open(os.getenv("HOME") + "/ws/wind_sensor/gcp/stats/day", "r").read()
    hour = open(os.getenv("HOME") + "/ws/wind_sensor/gcp/stats/hour", "r").read()
    return "<h1>Oscar's wind sensor data</h1><p><h4>Today's average reading is " + day + " units.</h4><p><a href='day'>Today's sensor data</a><p><h4>Last hour's average reading is " + hour + " units.</h4><p><a href='hour'>Last hour's sensor data</a>"

@app.route("/day", methods=['GET'])
def day():
    return render_template('current_day.html')

@app.route("/hour", methods=['GET'])
def hour():
    return render_template('current_hour.html')

@app.route("/", methods=['POST'])
def update_db():
    data = request.get_data().split("\n")
    if len(data) < 2:
        print("no data received")
        return "no data received\n"
    if (data[-1] != "&api-key=dev"):
        print("incorrect api key received")
        return "incorrect api key received\n"
    # Update database entry, overwrite if required
    for row in data:
        if len(row.split(",")) == 2 and validate_date(row.split(",")[0]):
            [capture_time, value] = row.split(",")
            print("processing " + capture_time + "," + str(value))
            mycursor.execute('INSERT INTO wind_sensor_data (capture_time, value)  VALUES ("' + capture_time + '","' + str(value) + '") ON DUPLICATE KEY UPDATE value="' + str(value) + '";')
        else:
            print("not processing row " + str(row))
    mydb.commit()
    print("post request received successfully")
    return "post request received successfully\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5100', debug=True)

