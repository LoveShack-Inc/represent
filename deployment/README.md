# Deployment

Currently we're using a cheap digital ocean instance. But we're not doing anything
"digital ocean" specific, so running this `setup.sh` script on any centos box 
should be enough to get this project started anywhere

### Setup

Run the setup script
```
setup.sh
```

That'll install all of the required deps, and clone the repo to `/opt/repp`

Build the containers
```
cd /opt/repp
docker-compose build
docker-compose up -d webservice \
  && sleep 5 \
  && docker-comopse up -d ui \
  && docker-compose up repp --crawl
```

The `ui` container has the static web content from the frontend build bundled in, 
and it'll run an nginx container that hosts it, and forwards anything to the `/api`
location to the webservice container

#### Basic auth (OPTIONAL)
If you want to setup basic auth, you can start the `ui` container with a couple of
env vars set. We set them for dev environments
```
NGINX_BASIC_USER=foo \
NGINX_BASIC_PASS=bar \
    docker-compose up -d ui
```
