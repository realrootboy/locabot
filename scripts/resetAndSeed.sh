#!/bin/bash

value="DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

docker exec locatrans psql -U postgres -d locabot -c "${value}"

python3 src/createDb.py

value=""

for f in migrations/*.sql; 
do 
  echo "Processing file: $f";
  value+=$(<$f) 
done

for f in seeds/*.sql; 
do 
  echo "Processing file: $f";
  value+=$(<$f) 
done

docker exec locatrans psql -U postgres -d locabot -c "${value}"