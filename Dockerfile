FROM python:3.8-alpine

ARG APP_HOME="/opt/repp"
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY . .

RUN pip install -e . \
  && mkdir $APP_HOME/database \
  && touch $APP_HOME/database/db.sqlite \
  && adduser -h $APP_HOME -D -H repp \
  && chown -R repp:repp $APP_HOME

USER repp
ENTRYPOINT 'repp'
