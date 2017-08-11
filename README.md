# djangp-tmpl

## Dependency

* python2.7/3
* django==1.11.4


``` bash
PROJECT_NAME=project
django-admin.py startproject --template=https://github.com/jarrekk/django-tmpl/archive/master.zip --extension=example,py,ini $PROJECT_NAME
cd $PROJECT_NAME/application
cp env.example .env
```

## Features

* logging
* celery
* django-environ
* django-debug-toolbar
* django-extension
* django-compressor
* django-anymail([MailGun](https://www.mailgun.com/)) with async function
* django-allauth(Email verify/login)
* django-rest-framework with jwt
* django class based views
* different settings for different environment
* different requirements for different environment
* MySQL support for each environment and sqlit3 for develop environment
* docker & docker-compose for development, test and production environment
* full user features with basic and rest