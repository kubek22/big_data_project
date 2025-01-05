#!/bin/bash

HQL_DIR="."
HIVE_CMD="hive -f"

for hql_file in "$HQL_DIR"/*.hql; do
    $HIVE_CMD "$hql_file"
    
    if [ $? -eq 0 ]; then
        echo "Successfully executed $hql_file"
    else
        echo "Failed to execute $hql_file" >&2
        exit 1
    fi
done

echo "All HQL scripts executed successfully."
