from datetime import datetime
import requests
import pandas as pd
import json
import boto3
import os
import math

s3_client = boto3.client('s3', aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
                         aws_secret_access_key=os.environ["AWS_SECRET_KEY"])

# Determine datestring
today = datetime.today()
monthstring = str(today.year) + str(today.month)
datestring = str(today.year) + str(today.month) + str(today.day)
timestring = str(math.floor(datetime.utcnow().hour/4)*4)

data_types = ["snowfall", "snowdensity", "snowdepth"]

geojson = {
    "type": "FeatureCollection",
    "features": []
}

# 3 key pages
"https://www.nohrsc.noaa.gov/nsa/discussions_text/National/snowdepth/" + monthstring
"https://www.nohrsc.noaa.gov/nsa/discussions_text/National/snowdensity/" + monthstring
"https://www.nohrsc.noaa.gov/nsa/discussions_text/National/snowdepth/" + monthstring

for data_type in data_types:
    # Create URL
    url = "https://www.nohrsc.noaa.gov/nsa/discussions_text/National/" + \
        data_type + "/" + datestring[0:6] + \
        "/" + data_type + "_" + datestring + timestring + "_e.txt"

    # Download file and remove first/last row
    try:
        downloadfile = requests.get(url)
        row_list = downloadfile.text.split("\n")
        row_list = row_list[1:-1]

        for row in row_list:
            row_ = row.split("|")
            try:
                if data_type == "snowfall":
                    feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [float(row_[3]), float(row_[2])]
                        },
                        "properties": {
                            "name": row_[1],
                            "elevation": row_[4],
                            "report_time_utc": row_[6],
                            "amount": row_[7],
                            "units": row_[8],
                            "duration": row_[9],
                            "durationunits": row_[10],
                        }
                    }
                else:
                    feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [float(row_[3]), float(row_[2])]
                        },
                        "properties": {
                            "name": row_[1],
                            "elevation": row_[4],
                            "report_time_utc": row_[6],
                            "amount": row_[7],
                            "units": row_[8],
                        }
                    }
                geojson["features"].append(feature)

            except:
                print(row_)

        filename = data_type + ".json"
        with open(filename, "w") as f:
            json.dump(geojson, f)

        response = s3_client.upload_file(
            filename, "graphsnowgeojson", filename)

    except Exception as e:
        print(e)
