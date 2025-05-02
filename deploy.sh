#!/bin/bash

set -a
source .env
set +a

IMAGE_NAME=trading_companion_prod:$VERSION
TAR_FILE=trading_companion_$VERSION.tar

docker buildx build --platform linux/arm64 --target=production -t $IMAGE_NAME .
docker save -o $TAR_FILE $IMAGE_NAME
scp $TAR_FILE alec@192.168.1.182:/home/alec/$TAR_FILE
rm $TAR_FILE

scp .env alec@192.168.1.182:/home/alec/.env
scp deploy_remote.sh alec@192.168.1.182:/home/alec/deploy_remote.sh
scp docker-compose.yml alec@192.168.1.182:/home/alec/docker-compose.yml

ssh alec@192.168.1.182 'sudo bash /home/alec/deploy_remote.sh'
