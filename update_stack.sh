git pull
docker-compose build

docker service update www_stack_fastapi
docker service update www_stack_svelte
docker service update www_stack_traefik

# docker stack deploy -c docker-compose.yml www_stack