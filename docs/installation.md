---
layout: default
title: Instalación
---

Es muy recomendable utilizar un entorno virtual tanto para
el desarrollo como para la puesta en producción. Te recomiendo dos
paquetes ampliamente difundidos para esto como son
[virtualenv](https://github.com/pypa/virtualenv)
y [virtualenvwrapper](https://bitbucket.org/virtualenvwrapper/virtualenvwrapper/)
que te permitirán gestionar fácilmente tus entornos virtuales.

Si utilizas [PyCharm](https://www.jetbrains.com/pycharm/)
puedes gestionar los entornos virtuales desde el propio
IDE (que internamente utiliza virtualenv).  

Para instalar **WordPlease** en tu máquina local para
desarrollar necesitarás realizar los siguientes pasos:

1. Clona el repositorio desde Github
2. Crea y activa un entorno virtual
3. Instala todas las dependencias necesarias
4. Crea la base de datos y un usuario administrador
5. Ejecuta el servidor Django

```bash

$ git clone https://github.com/tonybolanyo/wordplease.git
$ cd wordplease
$ mkvirtualenv wordplease
$ workon wordplease
$ pip install requirements.txt
$ cd src
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver

```

Si lo que quieres es instalarlo en una máquina en producción
lee las notas del apartado [Despliegue](deploy.md)