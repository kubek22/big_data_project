CREATE TABLE IF NOT EXISTS airbnb_data_parquet (
    id INT,
    name STRING,
    host_id INT,
    host_name STRING,
    neighbourhood STRING,
    latitude DOUBLE,
    longitude DOUBLE,
    room_type STRING,
    price INT,
    minimum_nights INT,
    number_of_reviews INT,
    last_review DATE,
    reviews_per_month DOUBLE,
    calculated_host_listings_count INT,
    availability_365 INT
)
PARTITIONED BY (neighbourhood_group STRING)
CLUSTERED BY (price) INTO 10 BUCKETS
STORED AS PARQUET
LOCATION '/project/airbnb/';
