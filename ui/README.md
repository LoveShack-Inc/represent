## UI

### Local Dev

#### Docker build
```bash
docker build . -t repp-ui
docker run -d -p 8090:80 repp-ui

# can view the site at localhost:8090, the backend won't work though
# by default
curl localhost:8090
```

#### Required deps
You'll need a working node/npm installation. It's easiest to use `nvm` to manage your 
npm installs if you don't already have your own workflow for it. 

Follow their docs [here](https://github.com/nvm-sh/nvm), or:
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.0/install.sh | bash
nvm install lts/fermium
nvm use lts/fermium
```

#### Setup vue cli (NOT REQURIED)

This only needs to be done once for the project, and I've already done it, so you won't 
have to.. I'm just documenting it here for posterity

```bash
# install vue-cli
npm install -g @vue/cli
vue create repp-ui
# choose the default options
```

------
# From the vue setup util

## Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Lints and fixes files
```
yarn lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
