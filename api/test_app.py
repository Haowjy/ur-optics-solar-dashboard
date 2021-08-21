import time
from flask import Flask, request, jsonify
import datetime
import pytz
import csv

from flask_pymongo import PyMongo
# my_date = datetime.datetime.now(pytz.timezone('US/New_York'))

global counter
counter = 0

app = Flask(__name__)

mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/solar_dashboard_database")
db = mongodb_client.db

# db.test.insert_one({'title': "todo title", 'body': "todo body"})
@app.route('/weather_many')
def weather_many():
    db.weather.insert_many([{
        "metadata": [{"sensorId": 5578}, {"type": "temperature"}],
        "timestamp": datetime.datetime.strptime("2021-05-18T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "temp": 12
        }, {
        "metadata": [{"sensorId": 5578}, {"type": "temperature"}],
        "timestamp": datetime.datetime.strptime("2021-05-18T04:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "temp": 11
        }, {
        "metadata": [{"sensorId": 5578}, {"type": "temperature"}],
        "timestamp": datetime.datetime.strptime("2021-05-18T08:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "temp": 11
        }, {
        "metadata": [{"sensorId": 5578}, {"type": "temperature"}],
        "timestamp": datetime.datetime.strptime("2021-05-18T12:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "temp": 12
        }, {
        "metadata": [{"sensorId": 5578}, {"type": "temperature"}],
        "timestamp": datetime.datetime.strptime("2021-05-18T16:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "temp": 16
        }, {
        "metadata": [{"sensorId": 5578}, {"type": "temperature"}],
        "timestamp": datetime.datetime.strptime("2021-05-18T20:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "temp": 15
        }, {
        "metadata": [{"sensorId": 5578}, {"type": "temperature"}],
        "timestamp": datetime.datetime.strptime("2021-05-19T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "temp": 13
        }, {
        "metadata": [{"sensorId": 5578}, {"type": "temperature"}],
        "timestamp": datetime.datetime.strptime("2021-05-19T04:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "temp": 12
        }, {
        "metadata": [{"sensorId": 5578}, {"type": "temperature"}],
        "timestamp": datetime.datetime.strptime("2021-05-19T08:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "temp": 11
        }, {
        "metadata": [{"sensorId": 5578}, {"type": "temperature"}],
        "timestamp": datetime.datetime.strptime("2021-05-19T12:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "temp": 12
        }, {
        "metadata": [{"sensorId": 5578}, {"type": "temperature"}],
        "timestamp": datetime.datetime.strptime("2021-05-19T16:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "temp": 17
        }, {
        "metadata": [{"sensorId": 5578}, {"type": "temperature"}],
        "timestamp": datetime.datetime.strptime("2021-05-19T20:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "temp": 12
        }])
    
    return jsonify(message="success")

@app.route('/test_time_insert')
def test_time_insert():
    # 157680000 second
    # print(datetime.datetime.strptime("7/12/2021 21:05", '%m/%d/%Y %H:%M'))
    db.test_time_series.insert_many([{"ts":datetime.datetime.strptime("7/12/2021 21:05", '%m/%d/%Y %H:%M'),"RECORD":2,"RZ_Global_Irr":148.3,"RZ_Direct_Irr":0,"RZ_Diffuse_Irr":148.3,"RZ_Pyrano_Temp_C":25.9,"RZ_Pyrhelio_Temp_C":24.3,"RZ_PRESS":1014,"RZ_Zenith_Ang":117.8642,"RZ_Azimuth_Ang":262.6575,"RZ_STAT":0,"RZ_HHMM":0,"Batt_V":13.51,"Panel_T":26.32},{"ts":datetime.datetime.strptime("7/12/2021 21:06", '%m/%d/%Y %H:%M'),"RECORD":3,"RZ_Global_Irr":181.9,"RZ_Direct_Irr":28.4,"RZ_Diffuse_Irr":181.9,"RZ_Pyrano_Temp_C":25.9,"RZ_Pyrhelio_Temp_C":24.3,"RZ_PRESS":1014,"RZ_Zenith_Ang":118.0516,"RZ_Azimuth_Ang":262.8085,"RZ_STAT":0,"RZ_HHMM":0,"Batt_V":13.52,"Panel_T":26.24}])
    # db.solar1min5year.insert_one()
    return jsonify(message="success")

@app.route("/test_weather_find")
def test_weather_find():
    # https://stackoverflow.com/questions/61217428/mongodb-how-to-query-a-time-series-with-incomplete-data
    test = db.weather.find()
    for t in test:
        print(t)
    return jsonify([t for t in test])


@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/livedata')
def get_sample_data():
    global counter
    counter += 1
    return {
        'time': datetime.datetime.now(pytz.timezone('America/New_York')),
        'irradiance' : {
            'global_horizontal': 0+counter,
            'direct_normal' : 0+counter,
            'diffuse_horizontal' : 0+counter,
        },
        'meteorological' : {
            'pr1_temperature' : 0+counter,
            'ph1_temperature': 0+counter,
            'pressure' : 0+counter,
            'zenith_angle' : 0+counter,
            'azimuth_angle' : 0+counter,
            'razon_status' : 0+counter,
            'razon_time' : 0+counter,
            'logger_battery' : 0+counter,
            'logger_temp' : 0+counter,
        },
        'units' : {
            'global_horizontal': "u",
            'direct_normal' : "u",
            'diffuse_horizontal' : "u",
            'pr1_temperature' : "u",
            'ph1_temperature': "u",
            'pressure' : "u",
            'zenith_angle' : "u",
            'azimuth_angle' : "u",
            'razon_status' : "u",
            'razon_time' : "u",
            'logger_battery' : "u",
            'logger_temp' : "u",
        }
    }

@app.route('/graph')
def get_sample_graph_data():
    # request.args.get('page', 1)
    arguments = {
        "irradiance-global-horizontal": 4,
        "irradiance-direct-normal": 5,
        "irradiance-diffuse-horizontal": 6,
        "meteorological-pr1-temperature": 7,
        "meteorological-ph1-temperature": 8,
        "meteorological-pressure": 9,
        "meteorological-zenith-angle": 10,
        "meteorological-azimuth-angle": 11,
        "meteorological-razon-status": 12,
        "meteorological-razon-time": 13,
        "meteorological-logger-battery": 14,
        "meteorological-logger-temp": 15    
    }

    includedData = [
        # 1,2,3,
        # 4,5,
        # 9,13
        ]

    for key, value in arguments.items():
        if(request.args.get(key) != None and request.args.get(key).lower()=="true"):
            includedData.append(value)

    print(includedData)

    headerDataDict = {
        "":0,
        "Year":1,
        "DOY":2,
        "MST":3,
        "Global Horizontal [W/m^2]":4,
        "Direct Normal [W/m^2]":5,
        "Diffuse Horizontal [W/m^2]":6,
        "PR1 Temperature [deg C]":7,
        "PH1 Temperature [deg C]":8,
        "Pressure [mBar]":9,
	    "Zenith Angle [degrees]":10,
        "Azimuth Angle [degrees]":11,
        "RaZON Status":12,
        "RaZON Time [hhmm]":13,
        "Logger Battery [VDC]":14,
        "Logger Temp [deg C]":15,
    }

    headerDataList = [
        "", # 0
        "Year",     # 1
        "DOY",      # 2
        "MST",      # 3
        "Global Horizontal [W/m^2]",    # 4
        "Direct Normal [W/m^2]",        # 5
        "Diffuse Horizontal [W/m^2]",
        "PR1 Temperature [deg C]", 
        "PH1 Temperature [deg C]",
        "Pressure [mBar]",              # 9
	    "Zenith Angle [degrees]",
        "Azimuth Angle [degrees]",
        "RaZON Status",
        "RaZON Time [hhmm]",            # 13
        "Logger Battery [VDC]",
        "Logger Temp [deg C]",
    ]

    irridianceDataList = ["Global Horizontal [W/m^2]",    # 4
        "Direct Normal [W/m^2]",        # 5
        "Diffuse Horizontal [W/m^2]",]

    meteorologicalDataList = ["PR1 Temperature [deg C]", 
        "PH1 Temperature [deg C]",
        "Pressure [mBar]",              # 9
	    "Zenith Angle [degrees]",
        "Azimuth Angle [degrees]",
        "RaZON Status",
        "RaZON Time [hhmm]",            # 13
        "Logger Battery [VDC]",
        "Logger Temp [deg C]",]

    graphList = []

    # print('hello')
    with open('20210629.csv') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        header = next(csv_reader)
        # print(header)
        # for h in header:
        #     graph[h] = []
        count = 1
        for lines in csv_reader:
            count+=1
            # if(count>10):
            #     break
        
            point = {}

            hour = lines[3][:-2]
            if(hour==""):
                hour = "0"
            dt = datetime.datetime.strptime(f"{lines[1]} {lines[2]} {hour}:{lines[3][-2:]}", '%Y %j %H:%M')
            dt= dt.replace(tzinfo=pytz.timezone('America/New_York'))

            point["date"] = dt.strftime('%x')
            # if(hour == "0" and lines[3][-2:]=="0"):
            #     point["date"] = dt.strftime('%x')
            
                # print("000000")
            # print(f"DT: {dt.strftime('%x')}")
            # print("Created at {:d}:{:02d}".format(int(hour), int(lines[3][-2:])))
            # print(dt.time())
            # dt.strftime("%-I:%M %p")

            point["datetime"] = dt.strftime("%I:%M %p").lstrip("0")
            # "{:d}:{:02d}".format(int(hour), int(lines[3][-2:]))

            # print(f"year: {lines[1]}\tdoy:{lines[2]}\tmst:{lines[3]}\t{lines[3][:-2]}...{lines[3][-2:]}")
            for include in includedData:
                point[headerDataList[include]] = float(lines[include])
            # print(point)
            graphList.append(point)
            # print(lines[4], lines[5], lines[13])

        includedHeaderStrings = {}

        irridianceHeaderStrings = []
        meteorologicalHeaderString = []
        for i,include in enumerate(includedData):
            includedHeaderStrings[headerDataList[include]] = i

            if(headerDataList[include] in irridianceDataList):
                irridianceHeaderStrings.append(headerDataList[include])

            elif(headerDataList[include] in meteorologicalDataList):
                meteorologicalHeaderString.append(headerDataList[include])

        print(includedHeaderStrings)
        print(irridianceHeaderStrings)
        print(meteorologicalHeaderString)

    return {"return_data":graphList, "included_headers":includedHeaderStrings, "irridiance_headers":irridianceHeaderStrings,"meteorological_headers":meteorologicalHeaderString}