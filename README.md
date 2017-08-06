# djangp-tmpl

## Dependency

* python2.7/3
* django==1.11.4


``` bash
PROJECT_NAME=project
django-admin.py startproject --template=https://github.com/jarrekk/django-tmpl/archive/master.zip --extension=example,py $PROJECT_NAME
cd $PROJECT_NAME/application
cp env.example .env
```

## Features

* logging
* celery
* email([MailGun](https://www.mailgun.com/))
* django-environ
* django-debug-toolbar
* django-extension
* django-compressor
* django-allauth(Email verify/login)
* django-rest-framework with jwt
* django class based views
* different settings for different environment
* different requirements for different environment
* docker & docker-compose
