from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("project") \
    .config("spark.hadoop.fs.webhdfs.impl", "org.apache.hadoop.hdfs.web.WebHDFS") \
    .config("spark.hadoop.fs.defaultFS", "http://localhost:50070") \
    .getOrCreate()

air_quality_path = "hdfs://node1/project/air_quality/"
airbnb_path = "hdfs://node1/project/airbnb/"
property_sales_path = "hdfs://node1/project/property_sales/"
geo_path = "hdfs://node1/project/geo/"

air_quality = spark.read.option("header", "true").csv(air_quality_path)
air_quality.printSchema()
air_quality.show()
print(f"Number of rows: {air_quality.count()}")

airbnb = spark.read.option("header", "true").csv(airbnb_path)

property_sales = spark.read.option("header", "true").csv(property_sales_path)

geo = spark.read.option("header", "true").csv(geo_path)

spark.stop()
