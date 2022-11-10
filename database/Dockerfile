FROM postgres:latest
ENV POSTGRES_PASSWORD=1234
ENV POSTGRES_USER=demo_user
ENV POSTGRES_DB=demo_db
COPY *.sql /docker-entrypoint-initdb.d/

