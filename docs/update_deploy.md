---
layout: default
title: Despliegue
---

Para actualizar a una nueva versión desde el repositorio
hay que seguir los siguientes pasos:

1. Conectar al servidor con ssh
2. Cambiar al usuario de la aplicación
3. Actualizar el código desde el repositorio
4. Activar el entorno virtual
5. Aplicar las migraciones
6. Actualizar los archivos estáticos
7. Compilar las traducciones
8. Reiniciar el servicio circus

Básicamente aplicar esta secuencia de comandos:

```
$ sudo -u wordplease -i
// como usuario wordplease
$ cd wordplease
$ git pull
$ cd src
$ pyenv activate env
$ python manage.py migrate
$ python manage.py collectstatic
$ python manage.py compilemessages
$ logout
// como usuario con permisos sudo
$ sudo service circusd restart
```