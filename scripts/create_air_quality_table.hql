CREATE EXTERNAL TABLE air_quality_avro (
    unique_id INT,
    indicator_id INT,
    name STRING,
    measure STRING,
    measure_info STRING,
    geo_join_id INT,
    geo_place_name STRING,
    time_period STRING,
    start_date DATE,
    data_value DOUBLE,
    message STRING
)
PARTITIONED BY (geo_type_name STRING)
CLUSTERED BY (geo_place_name) INTO 5 BUCKETS
STORED AS AVRO
LOCATION '/project/air_quality/';
