# djangp-tmpl

## Dependency

* python2.7/3
* django==1.11.4

## Quick start

``` bash
PROJECT_NAME=project
django-admin.py startproject --template=https://github.com/jarrekk/django-tmpl/archive/master.zip --extension=example,py,ini $PROJECT_NAME
cd $PROJECT_NAME/application
cp env.example .env
```

## Features

### Extensions

* django-extension
* django-environ
* django-debug-toolbar
* django-compressor
* django-htmlmin
* django-allauth(Email verify/login)
* django-anymail([MailGun](https://www.mailgun.com/)) with async function

### For development

* logging
* customized user model
* different settings for different environment
* different requirements for different environment
* Postgres support for each environment
* docker & docker-compose for development, test and production environment

### Rest API

* django-rest-framework with jwt
* django-rest-swagger at development & test environment

### Other

* celery
* django class based views(**Generics views**)
* full user features with basic views and rest API views
