---
layout: default
title: Notas adicionales
---

Al intentar hacer el despliegue y cambiar la base de datos de SQLite
a PostgreSQL se produce un error debido a las columnas `created`
y `updated` que vienen heredadas de la clase abstracta `TimeStampedModel`
en el modelo `Post`.

Un rápido vistazo a las migraciones pone de manifiesto que están heredadeas
en la migración `0001_initial.py` y luego vuelven a crearse
en `0002_auto_20171211_1753.py`. Aunque esto no genera un problema en
SQLite, sí lo hace en PostgreSQL.

Una solución sencilla es mezclar y optimizar las dos 
migraciones en cuestión.

Para ello, basta con utilizar el comando `squashmigrations`
que realizará esta optimización por nosotros según podemos
[leer en la documentación](https://docs.djangoproject.com/en/2.0/topics/migrations/#migration-squashing):

```bash
$ python manage.py squashmigrations blogs 0002
```

Esto crea una migración que sustituye a las dos primeras y, con
la optimización, el problema queda resuelto.

Una vez comprobado que la optimización no estropea nada ya se 
pueden borrar las migraciones anteriores.
