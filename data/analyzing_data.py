import pandas as pd

###

airbnb = pd.read_csv("airbnb/ab_nyc.csv")

airbnb.shape
airbnb.info()
airbnb.nunique()

# partition column
airbnb.neighbourhood_group

for val in airbnb.neighbourhood_group.unique():
    print(len(airbnb[airbnb.neighbourhood_group == val]))

###

air_quality = pd.read_csv("air_quality/air_quality.csv")

air_quality.shape
air_quality.info()
air_quality.nunique()

# partition columns
air_quality["Geo Type Name"]
# possibly "Start_Date"

for val in air_quality["Geo Type Name"].unique():
    print(len(air_quality[air_quality["Geo Type Name"] == val]))

###

sales = pd.read_csv("sales/nyc_rolling_sales.csv")

sales.shape
sales.info()
sales.nunique()

# partition columns
sales["SALE DATE"]
sales["BOROUGH"]

for val in sales["BOROUGH"].unique():
    print(len(sales[sales["BOROUGH"] == val]))

###

geo = pd.read_csv("geo/NHoodNameCentroids.csv")

geo.shape
geo.info()
geo.nunique()

