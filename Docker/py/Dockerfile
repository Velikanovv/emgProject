FROM python:alpine as API
COPY . /app
WORKDIR /app
RUN apk add --no-cache postgresql-libs libjpeg-turbo-dev zlib-dev &&\
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev &&\
    pip install -r requirements.txt --no-cache-dir &&\
    apk --purge del .build-deps     
EXPOSE 8000
CMD ./start.sh