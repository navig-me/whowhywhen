git pull
docker-compose build

docker stack rm www_stack
docker stack deploy -c docker-compose.yml www_stack