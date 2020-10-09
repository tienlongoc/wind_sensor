import argparse, sys
from datetime import datetime
import mysql.connector
import plotly.graph_objects as go
import numpy as np
import os

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

def mean(l):
    return float(sum(list(map(int, l))))/float(len(list(map(int, l))))

def generate_daily_report(day):
    mycursor.execute("SELECT * FROM wind_sensor_data WHERE capture_time LIKE '" + day + "%';")
    data = np.array(list(mycursor.fetchall()))
    if (len(data) == 0):
        return True
    x = data[:,0]
    y = data[:,1]
    hourly_y = []
    curr_hour_mark = x[0][:11]
    hourly_x = [datetime.strptime(curr_hour_mark, "%Y%m%d-%H")]
    curr_hour_values = []
    for i in range(len(x)):
        if x[i][:11] != curr_hour_mark:
            curr_hour_mark = x[i][:11]
            hourly_y.append(mean(curr_hour_values))
            hourly_x.append(datetime.strptime(curr_hour_mark, "%Y%m%d-%H"))
            curr_hour_values = []
        curr_hour_values.append(y[i])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hourly_x,y=hourly_y,name="Normalised hourly values"))
    fig.update_layout(
        title = 'Wind speed data for date ' + day,
        xaxis = dict(
            title = 'Time',
            titlefont_size=16,
            tickfont_size=14,
        ),
        yaxis=dict(
            title = 'Wind speed unit',
            titlefont_size=16,
            tickfont_size=14,
        )
    )
    fig.write_html(os.getenv("HOME") + "/ws/wind_sensor/gcp/charts/daily/" + day + ".html")
    
    with open(os.getenv("HOME") + "/ws/wind_sensor/gcp/stats/day", "w") as f:
        f.write(str("%.2f" % mean(y)))

def generate_hourly_report(hour):
    mycursor.execute("SELECT * FROM wind_sensor_data WHERE capture_time LIKE '" + hour + "%';")
    data = np.array(list(mycursor.fetchall()))
    if (len(data) == 0):
        return True
    x = [datetime.strptime(t, '%Y%m%d-%H:%M') for t in data[:,0]]
    y = data[:,1]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x,y=y,name="Minute values"))
    fig.update_layout(
        title = 'Wind speed data for hour ' + hour,
        xaxis = dict(
            title = 'Time',
            titlefont_size=16,
            tickfont_size=14,
        ),
        yaxis=dict(
            title = 'Wind speed unit',
            titlefont_size=16,
            tickfont_size=14,
        )
    )
    fig.write_html(os.getenv("HOME") + "/ws/wind_sensor/gcp/charts/hourly/" + hour + ".html")

    with open(os.getenv("HOME") + "/ws/wind_sensor/gcp/stats/hour", "w") as f:
        f.write(str("%.2f" % mean(y)))

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
