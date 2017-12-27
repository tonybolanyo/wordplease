---
layout: default
title: WordPlease
---

# Sobre la implementación de la lista de blogs

Mi primera idea era utilizar el método [`.distinct()`](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#distinct)
en un queryset de Django. El caso es que con SQLite no puede usarse DISTINCT ON, lo que provoca una exceptión
`NotImplementedError: DISTINCT ON fields is not supported by this database backend` así que lo mejor era buscar
otra opción.

Una posiblidad era crear un nuevo modelo `Blog` que permitiese vincular un usuario con sus artículos y que, además,
permitiría tener más de un blog por usuario. En el enunciado esta posibilidad no queda clara, aunque por aclaración
de @kas sería una implementación válida.

Aún así es posible relizarlo de una segunda forma alternativa. La opción es realizar un `groupby` y encontrar el último
post publicado por cada autor. Esto además nos permite mostrar fácilmente en el listado de blogs disponibles el último
artículo publicado por cada autor.

