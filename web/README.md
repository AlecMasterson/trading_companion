## Docket Setup

docker run --name trading_companion_web --rm -itd --mount type=bind,source="$(pwd)",target=/web -p 3000 node:18.3.0

docker compose run --rm -itd -p 3000:3000 web
