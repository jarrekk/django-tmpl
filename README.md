# djangp-tmpl

## Dependency

* python2.7/3
* django==1.11.4

## Generic views template

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
* django-allauth(Email verify/login)
* django-anymail([MailGun](https://www.mailgun.com/)) with async function

### For development

* logging
* different settings for different environment
* different requirements for different environment
* MySQL support for each environment and sqlit3 for develop environment
* Postgres support for each environment.
* docker & docker-compose for development, test and production environment

### Rest API

* django-rest-framework with jwt

### Other

* celery
* django class based views(**Generics views**)
* full user features with basic views and rest API views

### Go to [MySQL Generic views](https://github.com/jarrekk/django-tmpl/tree/GenericView_MySQL)
### Go to [APIView template](https://github.com/jarrekk/django-tmpl/tree/APIView)
