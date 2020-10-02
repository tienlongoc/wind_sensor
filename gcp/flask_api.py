from flask import Flask, request
import mysql.connector
from datetime import datetime

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
        if date_text != datetime.strptime(date_text, "%Y%m%d-%H:%M:%S").strftime('%Y%m%d-%H:%M:%S'):
            raise ValueError
        return True
    except ValueError:
        return False

@app.route("/", methods=['GET'])
def home():
    return "<h1>Oscar's API</h1>"


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
