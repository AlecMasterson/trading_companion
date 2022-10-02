## Docket Setup

docker run --name trading_companion_web --rm -itd --mount type=bind,source="$(pwd)",target=/web -p 3000 node:18.3.0
