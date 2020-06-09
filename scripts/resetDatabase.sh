#!/bin/bash

docker start locatrans

value="DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

docker exec locatrans psql -U postgres -d locabot -c "${value}"

python3 src/createDb.py

value=""

for f in migrations/*.sql; 
do 
  echo "Processing $f file..";
  value+=$(<$f) 
done

docker exec locatrans psql -U postgres -d locabot -c "${value}"