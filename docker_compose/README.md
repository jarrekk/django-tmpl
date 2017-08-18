# Docker Compose for django application

## Development

``` bash
docker-compose up
```

* Run project with PyCharm
* Run celery with command `celery -A taskapp worker -B -l info` at **application** folder.

## Test & Production

``` bash
docker-compose build
docker-compose start
```
