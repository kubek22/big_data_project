#!/bin/bash

chmod +x ./create_hadoop_directories.sh ./define_hbase_tables.sh

./create_hadoop_directories.sh
./define_hbase_tables.sh

echo "All scripts executed successfully!"
