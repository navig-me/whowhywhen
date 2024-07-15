# Stage 1: Build the Svelte app
FROM node:21 AS builder

WORKDIR /app
COPY ./who-why-when-landing-page /app

RUN npm install
RUN npm run build

# Stage 2: Serve the Svelte app with Caddy
FROM caddy:2.4.6-alpine

COPY --from=builder /app/public /srv
COPY Caddyfile /etc/caddy/Caddyfile

EXPOSE 80
EXPOSE 443

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]
