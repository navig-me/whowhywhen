# Pull the latest changes from the Git repository
git pull

# Build the Docker images
docker-compose build

# Remove the existing services from the stack
docker service rm www_stack_dash
docker service rm www_stack_api
docker service rm www_stack_svelte
docker service rm www_stack_traefik
docker service rm www_stack_celery
docker service rm www_stack_celery_beat
docker service rm www_stack_redis
docker service rm www_stack_flower

# Deploy the updated stack
docker stack deploy -c docker-compose.yml www_stack
