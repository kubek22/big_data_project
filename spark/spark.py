from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import regexp_replace, trim, lower, udf
from pyspark.sql.types import BooleanType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("project") \
    .config("spark.hadoop.fs.webhdfs.impl", "org.apache.hadoop.hdfs.web.WebHDFS") \
    .config("spark.hadoop.fs.defaultFS", "http://localhost:50070") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Define paths
air_quality_path = "hdfs://node1/project/air_quality/"
airbnb_path = "hdfs://node1/project/airbnb/"
property_sales_path = "hdfs://node1/project/property_sales/"
geo_path = "hdfs://node1/project/geo/"

# Load data from HDFS
air_quality = spark.read.option("header", "true").csv(air_quality_path).na.drop()
airbnb = spark.read.option("header", "true").csv(airbnb_path).na.drop()
geo = spark.read.option("header", "true").csv(geo_path).na.drop()
property_sales = spark.read.option("header", "true").csv(property_sales_path).na.drop()

# Clean and standardize neighborhood names
property_sales = property_sales.withColumn("neighborhood", trim(regexp_replace(lower(F.col("neighborhood")), "[^a-zA-Z0-9 ]", "")))
air_quality = air_quality.withColumn("geo_place_name", trim(regexp_replace(lower(F.col("geo_place_name")), "[^a-zA-Z0-9 ]", "")))
geo_borough = geo.select("name", "borough").withColumnRenamed("name", "neighborhood")
geo_borough = geo_borough.withColumn("neighborhood", trim(regexp_replace(lower(F.col("neighborhood")), "[^a-zA-Z0-9 ]", "")))

# UDF to check if a string contains another
@udf(BooleanType())
def string_contains(property_neighborhood, geo_neighborhood):
    return geo_neighborhood in property_neighborhood

# Perform the join using the custom UDF and disambiguate column references
property_sales_with_borough = property_sales.alias("ps").crossJoin(geo_borough.alias("gb")) \
    .filter(string_contains(F.col("ps.neighborhood"), F.col("gb.neighborhood"))) \
    .select(F.col("ps.neighborhood"), F.col("gb.borough"), F.col("ps.sale_price")).dropDuplicates()

# Perform the join for air quality data
air_quality_with_borough = air_quality.alias("aq").crossJoin(geo_borough.alias("gb")) \
    .filter(string_contains(F.col("aq.geo_place_name"), F.col("gb.neighborhood"))) \
    .select(F.col("aq.geo_place_name").alias("neighborhood"), F.col("gb.borough"), F.col("aq.name"), F.col("aq.data_value")).dropDuplicates()

# Check if the join worked
property_sales_with_borough.show()
air_quality_with_borough.show()

# Use the existing borough column in airbnb data
airbnb_with_borough = airbnb.withColumnRenamed("neighbourhood_group", "borough")

# Register dataframes as SQL tables
airbnb_with_borough.createOrReplaceTempView("airbnb")
property_sales_with_borough.createOrReplaceTempView("property_sales")
air_quality_with_borough.createOrReplaceTempView("air_quality")

# Example SQL queries to analyze the data

# Query 1: Average Airbnb price per neighborhood with borough
airbnb_avg_price_query = """
SELECT neighbourhood, borough, AVG(CAST(price AS INT)) as avg_airbnb_price
FROM airbnb
GROUP BY neighbourhood, borough
ORDER BY avg_airbnb_price DESC
"""
avg_airbnb_price_df = spark.sql(airbnb_avg_price_query)

# Query 2: Count of Airbnb listings by neighborhood with borough
airbnb_listing_count_query = """
SELECT neighbourhood, borough, COUNT(id) as total_listings
FROM airbnb
GROUP BY neighbourhood, borough
ORDER BY total_listings DESC
"""
listing_count_df = spark.sql(airbnb_listing_count_query)

# Query 3: Average property sales price by neighborhood with borough
property_sales_avg_price_query = """
SELECT neighborhood, borough, AVG(CAST(sale_price AS INT)) as avg_sale_price
FROM property_sales
GROUP BY neighborhood, borough
ORDER BY avg_sale_price DESC
"""
avg_sale_price_df = spark.sql(property_sales_avg_price_query)

# Query 4: Distribution of property sales prices by neighborhood with borough
property_sales_price_distribution_query = """
SELECT neighborhood, borough, MIN(CAST(sale_price AS INT)) as min_sale_price, 
       MAX(CAST(sale_price AS INT)) as max_sale_price, 
       AVG(CAST(sale_price AS INT)) as avg_sale_price
FROM property_sales
GROUP BY neighborhood, borough
ORDER BY avg_sale_price DESC
"""
price_distribution_df = spark.sql(property_sales_price_distribution_query)

# Query 5: Aggregate air quality data for Fine particles (PM 2.5) by neighborhood with borough
air_quality_agg_query = """
SELECT neighborhood, borough, SUM(CAST(data_value AS FLOAT)) as total_pm25_value
FROM air_quality
WHERE name = 'Fine particles (PM 2.5)'
GROUP BY neighborhood, borough
ORDER BY total_pm25_value DESC
"""
air_quality_agg_df = spark.sql(air_quality_agg_query)

#Show the results
avg_airbnb_price_df.show()
listing_count_df.show()
avg_sale_price_df.show()
price_distribution_df.show()
air_quality_agg_df.show()

# Coalesce the DataFrame to a single partition and then save it to HDFS as a single CSV file
avg_airbnb_price_df.coalesce(1).write.option("header", "true").mode("overwrite").format("csv").save("hdfs://node1/project/output/avg_airbnb_price")
listing_count_df.coalesce(1).write.option("header", "true").mode("overwrite").format("csv").save("hdfs://node1/project/output/listing_count")
avg_sale_price_df.coalesce(1).write.option("header", "true").mode("overwrite").format("csv").save("hdfs://node1/project/output/avg_sale_price")
price_distribution_df.coalesce(1).write.option("header", "true").mode("overwrite").format("csv").save("hdfs://node1/project/output/price_distribution")
air_quality_agg_df.coalesce(1).write.option("header", "true").mode("overwrite").format("csv").save("hdfs://node1/project/output/air_quality_agg")

spark.stop()
