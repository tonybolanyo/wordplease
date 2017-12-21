---
layout: default
title: Registro, login y logout
---

Desde la versión 1.11 Django tiene implementadas algunas
vistas basadas en clases para gestionar las cuestiones
básicas de login, logout o cambios de contraseña.
[Leer documentación](https://docs.djangoproject.com/en/2.0/topics/auth/default/#module-django.contrib.auth.views).

Para implementar el sistema de acceso, las vistas login y
logout están implementadas heredando de dichas vistas genéricas.

En el caso del registro de usuario Django no aporta ninguna
vista específica, pero sí un formulario que podemos utilizar.
El formulario `SignupForm` hereda del formulario `UserCreationForm`
mencionado.

También ha resultado necesario crear las plantillas ya que Django
no las proporciona.
