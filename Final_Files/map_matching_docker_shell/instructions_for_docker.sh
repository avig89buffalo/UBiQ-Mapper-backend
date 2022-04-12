docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-extract -p /opt/car.lua /data/new-york-latest.osm.pbf

docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-partition /data/new-york-latest.osrm

docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-customize /data/new-york-latest.osrm

docker run -t -i -p 5000:5000 -v "${PWD}:/data" osrm/osrm-backend osrm-routed --algorithm mld --max-matching-size 5000 /data/new-york-latest.osrm