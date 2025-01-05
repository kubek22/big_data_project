#!/bin/bash

echo "create 'air_quality', 'm', 'g', 't'" | hbase shell
echo "create 'airbnb', 'r', 'g'" | hbase shell
echo "create 'property_sales', 'p', 'g'" | hbase shell
echo "create 'geo', 'g'" | hbase shell


