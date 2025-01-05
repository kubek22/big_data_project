CREATE TABLE IF NOT EXISTS geo_parquet (
    geom STRING,
    object_id INT,
    name STRING,
    stacked INT,
    line1 STRING,
    line2 STRING,
    line3 STRING,
    angle INT,
    borough STRING
)
STORED AS PARQUET
LOCATION '/project/geo/';
