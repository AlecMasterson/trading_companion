#!/bin/bash

sed -i 's/\r$//' /home/alec/.env
set -a
source /home/alec/.env
set +a

sudo docker load -i /home/alec/trading_companion_$VERSION.tar
sudo docker tag trading_companion_prod:$VERSION trading_companion:latest
rm /home/alec/trading_companion_$VERSION.tar
