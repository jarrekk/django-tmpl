# djangp-tmpl

## Dependency

* python2.7/3
* django==1.11.4


``` bash
django-admin.py startproject --template=https://github.com/jarrekk/django-tmpl/archive/master.zip --extension=example,py project
cd project/application
cp env.example .env
```

## Features

* logging
* celery
* email([MailGun](https://www.mailgun.com/))
* django-environ
* django-debug-toolbar
* django-compressor
* different settings for different environment
* different requirements for different environment
* docker & docker-compose
