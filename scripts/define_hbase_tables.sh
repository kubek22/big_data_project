#!/bin/bash

echo "create 'air_quality', 'd'" | hbase shell
echo "create 'airbnb', 'r', 'g'" | hbase shell
echo "create 'property_sales', 'd'" | hbase shell
echo "create 'geo', 'd'" | hbase shell


