#!/bin/bash

lxterminal --command="/bin/bash -c 'source ~/ParkingManagement/env/bin/activate; 
trap deactivate EXIT;
cd ~/ParkingManagement/database/;
python flask_server.py; 
exec bash'"

lxterminal --command="/bin/bash -c 'source ~/ParkingManagement/env/bin/activate;
trap deactivate EXIT;
python ~/ParkingManagement/main2.py;
exec bash'"