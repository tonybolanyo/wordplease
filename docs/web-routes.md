---
layout: default
title: Rutas de la web
---

Además de la página principal de portada que muestra los
últimos artículos publicados, WordPlease tiene definidas
las siguientes rutas:

- `/blogs/`: muestra una lista con todos los blogs de usuario
  disponibles. En la especificación inicial se especifica
  implícitamente un blog por usuario, así que el diseño
  más simple es mostrar los usuarios *únicos* que 
  tienen publicado algún artículo.
- `/blogs/<author-name>/`: muestra una lista de todos los 
  artículos publicados por un autor ordenados por fecha
  de publicación, primero los artículos más recientes.
  El nombre del autor se recibe como parte de la ruta.
- `/blogs/<author-name>/<post-id>`: muestra un artículo completo
- `/new-post/`: permite crear un nuevo post a un autor
  que ha iniciado sesión
- `/login`: formulario de login para usuarios registrados.
- `/logout`: permite a un usuario desconectarse y cerrar sesión.
- `/signup`: permite a un usuario nuevo registrarse en la plataforma.

