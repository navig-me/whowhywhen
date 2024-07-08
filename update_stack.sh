git pull
docker-compose build

docker service rm www_stack_fastapi
docker service rm www_stack_svelte
docker service rm www_stack_traefik

docker stack deploy -c docker-compose.yml www_stack