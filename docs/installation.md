---
layout: default
title: WordPlease web routes
---

It's strongly recommended that you use a virtual environment
either in a development machine or in production server. I personally
recommend [virtualenv](https://github.com/pypa/virtualenv)
and [virtualenvwrapper](https://bitbucket.org/virtualenvwrapper/virtualenvwrapper/)
packages for an easy virtual environments management.

If you use [PyCharm](https://www.jetbrains.com/pycharm/) you can use
its own virtual environments manager.  

To install WordPlease on your local machine for development
you need to perform the following steps:

1. Clone the github repository
2. Create and activate a virtual environment
3. Install all required dependencies
4. Create database
5. Run the Django Server

```bash

$ git clone https://github.com/tonybolanyo/wordplease.git
$ cd wordplease
$ mkvirtualenv wordplease
$ workon wordplease
$ pip install requirements.txt
$ cd src
$ python manage.py migrate
$ python manage.py runserver

```