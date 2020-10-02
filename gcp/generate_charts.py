import argparse, sys
from datetime import datetime
import mysql.connector
import plotly.graph_objects as go
import numpy as np

mydb = mysql.connector.connect(
  host="localhost",
  user="wind_sensor",
  passwd="password",
  database="wind_sensor_db"
)
mycursor = mydb.cursor(buffered=True)

def validate_date(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y%m%d").strftime('%Y%m%d'):
            raise ValueError
        return True
    except ValueError:
        return False

def validate_hour(hour_text):
    try:
        if hour_text != datetime.strptime(hour_text, "%Y%m%d-%H").strftime('%Y%m%d-%H'):
            raise ValueError
        return True
    except ValueError:
        return False


def generate_daily_report(day):
    mycursor.execute("SELECT * FROM wind_sensor_data WHERE capture_time LIKE '" + day + "%';")
    data = np.array(list(mycursor.fetchall()))
    if (len(data) == 0):
        return True
    x = [datetime.strptime(t, '%Y%m%d-%H:%M:%S') for t in data[:,0]]
    y = data[:,1]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x,y=y))
    fig.write_html("./charts/daily/" + day + ".html")


def generate_hourly_report(hour):
    mycursor.execute("SELECT * FROM wind_sensor_data WHERE capture_time LIKE '" + hour + "%';")
    data = np.array(list(mycursor.fetchall()))
    if (len(data) == 0):
        return True
    x = [datetime.strptime(t, '%Y%m%d-%H:%M:%S') for t in data[:,0]]
    y = data[:,1]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x,y=y))
    fig.write_html("./charts/hourly/" + hour + ".html")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Input date or hour to proceed with chart generation")
    parser.add_argument("--day", type=str, help="Generate chart based on given date.", default="NA")
    parser.add_argument("--hour", type=str, help="Generate chart based on given hour.", default="NA")
    args = parser.parse_args()

    if (args.day == "NA" and args.hour =="NA") or (args.day != "NA" and args.hour !="NA"):
        print("Please supply only one parameter (day or hour)")
        sys.exit(1)


    if (args.day != "NA"):
        if not validate_date(args.day):
            print("Incorrect day format received. Must be %Y%m%d")
            sys.exit(1)
        generate_daily_report(args.day)

    if (args.hour != "NA"):
        if not validate_hour(args.hour):
            print("Incorrect hour format received. Must be %Y%m%d-%H")
            sys.exit(1)
        generate_hourly_report(args.hour)
