# Docker Compose for django application

## Development

``` bash
docker-compose up
```

* Run project with PyCharm
* Run celery with command `celery -A taskapp worker -B -l info` at **application** folder.

## Test & Production

* Edit Dockerfile & celery.dockerfile: *ENV* variable

``` bash
docker-compose -f docker-compose-all.yml build
docker-compose -f docker-compose-all.yml restart
```
