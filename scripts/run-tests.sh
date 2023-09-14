# ./scripts/run-tests.sh
pytest_args=$*
docker compose -f docker-compose.yml run --build --rm app-test $pytest_args
docker compose -f docker-compose.yml --profile test down --volumes