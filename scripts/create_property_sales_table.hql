CREATE TABLE property_sales_avro (
    unnamed_0 INT,
    neighborhood STRING,
    building_class_category STRING,
    tax_class_at_present STRING,
    block INT,
    lot INT,
    easement STRING,
    building_class_at_present STRING,
    address STRING,
    apartment_number STRING,
    zip_code INT,
    residential_units INT,
    commercial_units INT,
    total_units INT,
    land_square_feet INT,
    gross_square_feet INT,
    year_built INT,
    tax_class_at_time_of_sale INT,
    building_class_at_time_of_sale STRING,
    sale_price INT, -- empty string values
    sale_date DATE
)
PARTITIONED BY (borough INT)
CLUSTERED BY (neighborhood) INTO 10 BUCKETS
STORED AS PARQUET
LOCATION '/project/property_sales/';
