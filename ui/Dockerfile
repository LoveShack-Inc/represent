FROM node:fermium-alpine3.10 as builder

COPY ["package.json", "yarn.lock", "./"]

RUN mkdir /opt/repp
WORKDIR /opt/repp

# If I don't set this, then yarn creates the node_modules folder at the 
# root of the filesystem, which causes it to fail later when we run `yarn lint`
# and `yarn build`. I don't really get why that's it's default behavior, but
# this handles it
RUN yarn install --modules-folder ./node_modules

COPY . .

RUN yarn lint \
  && yarn build


####
FROM nginx:stable-alpine 

COPY --from=builder /opt/repp/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
