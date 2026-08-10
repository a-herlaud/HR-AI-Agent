FROM docker.io/library/postgres:15-alpine

COPY init.sh /docker-entrypoint-initdb.d/init.sh

RUN chmod +x /docker-entrypoint-initdb.d/init.sh