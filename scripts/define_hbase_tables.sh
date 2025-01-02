#!/bin/bash

echo "create 'air_quality', 'meas', 'geo', 'date'" | hbase shell
echo "create 'airbnb', 'room', 'geo'" | hbase shell
echo "create 'property_sales', 'prop', 'geo', 'info'" | hbase shell


