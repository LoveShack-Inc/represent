FROM python:3.8-alpine

ARG APP_HOME="/opt/repp"
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY . .

# these are literally all to support pdfplubmer, which
# depends on Pillow, and Pillow requires a bunch of crap
RUN apk add \
  --virtual .build-deps --no-cache \
    build-base \
    python3-dev \
    zlib-dev \
    jpeg-dev

RUN pip install -e . \
  && mkdir $APP_HOME/database \
  && touch $APP_HOME/database/db.sqlite \
  && adduser -h $APP_HOME -D -H repp \
  && chown -R repp:repp $APP_HOME \ 
  && apk del .build-deps


USER repp
ENTRYPOINT 'repp'
