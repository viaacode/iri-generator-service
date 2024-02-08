# ./scripts/run-dev.sh
docker compose -f docker-compose.yml --profile dev up --build "$@"