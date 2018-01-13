---
layout: default
title: Despliegue
---

Here you can read some notes I take while deploying nodepop on a free tier AWS server.

# Crear máquina virtual

- Entrar en aws.amazon.com y, en el apartado de EC2, crear una nueva instancia con el AMI: **Ubuntu Server 16.04 LTS (HVM), SSD Volume Type** - ami-da05a4a0
- Usar la instancia **t2.micro** que es válida para el **Free tier**
- Las opciones de configuración por defecto son válidas, pero asegúrate de que se asigna una dirección IP y **marca la opción Protect against accidental termination** para evitar eliminar la máquina por error.
- Agregar un disco. Como vamos a utilizar muy pocas cosas en la práctica, con los 8Gb que asigna por defecto debería ser suficiente.
- En el último paso puedes agregar una etiqueta a la instacia, por si quieres tenerlas clasificadas de alguna manera.
- Por último, en los grupos de seguridad, puedes reutilizar el grupo que utilizamos en clase, pero por cuestión de práctica vamos a crear uno nuevo: kc-tony
- Al crear el grupo de seguridad ya nos indica la apertura del puerto 22 para SSH. Como ya sabemos que vamos a utilizar la web (puerto 80) y que queremos usar un puerto alternativo para el SSH, podemos abrirlos directamente aquí.
    - Puerto 80 para la web
    - Puerto XXXX para el SSH (ojo, no quites el 22, hay que configurar primero el servicio en el sistema operativo para que use este puerto en lugar del 22).

En la pantalla de revisión nos alerta de que el servidor está accesible desde cualquier parte del mundo. Esto podemos solucionarlo solamente si tenemos una IP estática desde la que vamos a conectarnos. En caso contrario este es precisamente el comportamiento que deseamos.

**¡Ya puedes lanzar la máquina!**

Puedes generar un par de claves propias para acceder a la máquina o reutilizar un par existente. Crearemos un nuevo par solamente para este propósito.

Si todo ha ido bien, recibirás un mensaje de que la máquina está lanzándose y, en poco tiempo, (menos de un minuto) tu máquina estará funcionando.

# Conexión mediante ssh

Desde el terminal podemos conectarnos usando la clave privada con el siguiente comando:

```bash
$ ssh -i <ruta a kc-devops.pem> ubuntu@<ip o dns de la máquina>
```
## Primeras acciones

### Actualizar el sistema

Lo primero que voy a hacer es actualizar el sistema utilizando `apt-get`

```bash
$ sudo apt-get update
$ sudo apt-get upgrade
```
Para hacerlo todo en una sola instrucción:

```bash
$ sudo apt-get update && sudo apt-get upgrade -y
```
### Cambiar el puerto de acceso ssh

Esta es una operación delicada, ya que podemos perder el acceso a la máquina si no tenemos cuidado.

Lo primero será editar el archivo de configuración del servicio ssh:

```bash
$ sudo vim /etc/ssh/sshd_config
```

Lo que hay que cambiar es el puerto, así que buscamos la línea que indica `Port 22`, que se encuentra al principio del archivo y lo cambiamos por el número de puerto que queremos usar, en este caso el XXXX, que es el que hemos abierto en el firewall del grupo de seguridad al crear la máquina virtual.

```
Port XXXX
```

Una vez modificado el archivo hay que recargar el servicio SSH. Como esta operación es delicada, es mejor utilizar `reload` que `restart` ya que el segundo nos cerraría la sesión remota actual impidiéndonos arreglar cualquier cosa que fallase en la configuración.

```bash
$ sudo service ssh reload
```

Para probar que toda la configuración es correcta vamos a abrir **otra conexión ssh sin cerrar la actual** y, en este caso debemos especificar el puerto con el modificador `-p`

```bash
$ ssh -i <ruta/archivo.pem> -p <puertossh> ubuntu@<ipservidor>
```

Si todo ha ido bien, esta será la forma de conexión a partir de ahora y podemos cerrar la conexión anterior. En caso contrario, esta segunda conexión no se abrirá y podemos usar la primera para solucionar cualquier problema de configuración.

**Si alguna vez perdemos el acceso a la máquina por SSH** y necesitamos configurar de nuevo el servicio, el mecanismo que podemos usar sería conectar el disco a otra máquina virtual y editar los archivos de configuración desde la otra máquina. Volviendo a poner el disco en la máquina original cuando hayamos acabado de reconfigurar.

# Instalar paquetes necesartios

Lo primero será instalar postgreSQL, nginx y algunas librerías adicionales necesarias para compilar python.

```
$ sudo apt-get install postgresql nginx build-essential zlib1g-dev libssl-dev libbz2-dev libreadline-dev libsqlite3-dev python-setuptools circus
```

# Crear un usuario para la aplicación

Para controlar los permisos de la aplicación es recomendable utilizar un usuario para la propia aplicación, así que vamos a crearlo, pero impidiendo que pueda hacer login en la consola. Además lo incluiremos en el grupo de nginx (normalmente www-data)

```
$ sudo adduser wordplease
$ sudo passwd -l wordplease
$ sudo adduser www-data wordplease
```

El siguiente paso es crear la base de datos y un usuario en ella para los datos de la aplicación:

```
$ sudo -u postgres createuser wordplease
$ sudo -u postgres createdb wordplease -O wordplease
```

# Clonar la aplicación en el directorio del usuario de la aplicación

Lo primero será identificarnos como el usuario en cuestión

```
$ sudo -u wordplease -i
```

## Instalación de pyenv

Esto nos permite instalar cualquier versión de Python fácilmente y, por supuesto, crear diferentes entornos separados.

```
$ git clone https://github.com/yyuu/pyenv.git ~/.pyenv
$ git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
```

Después de eso, hay que preparar el perfil de bash para cada inicio de sesión, de forma que utilice pyenv:

```
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
$ echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
$ echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
```

Para que los cambios surjan efecto cerramos la sesión del usuario y la volvemos a abrir:

```
$ logout
$ sudo -u wordplease -i
```

Ahora ya podemos instalar la versión de Python que necesitemos, en nuestro caso vamos a usar la última disponible y después crear un entorno virtual:

```
$ pyenv install 3.6.4
$ pyenv virtualenv 3.6.4 env
```

## Instalando la aplicación desde GitHub

Lo primero será clonar el repositorio de GitHub, pero como no necesitamos
toda la historia del desarrollo, vamos a hacerlo, indicando
a git que solamente se descargue el último commit:

```
$ git clone --depth=1 https://github.com/tonybolanyo/wordplease.git
```

También vamos a crear una carpeta `logs` para tener todos
los logs relativos a nuestra app en un solo sitio.

```
$ mkdir logs
```

Es el momento de activar el entorno virtual e instalar las
dependencias, agregando además `gunicorn` para poder
servir nuestra aplicación.

```
// como usuario wordplease
$ pyenv activate env
$ pip install -r wordplease/requirements.txt
$ pip gunicorn
```

El siguiente paso será aplicar las migraciones, recopilar los archivos
estáticos y crear un
superusuario, pero antes necesitamos crear las variables
de entorno que va a utilizar nuestra aplicación (podemos
obviar de momento los correos electrónicos, pero no los
relativos a la base de datos, secret key y el archivo
settings a utilizar).

```
$ export SECRET_KEY=<secret_key>
$ export DB_NAME=wordplease
$ export DB_USER=wordplease
$ export DJANGO_SETTINGS_MODULE=wordplease.settings_production

$ cd wordplease/src
$ python manage.py migrate
$ python manage.py collectstatic --noinput
$ python manage.py createsuperuser
```

Ahora ya podemos cerrar la sesión del usuario `wordplease` y
volver a nuestro usuario con capacidades de `sudo`.

```
$ pyenv deactivate
$ logout
```

# Circus, gunicorn y nginx

## Configuración de gunicorn

Creamos un archivo de configuración para la aplicación:

```
$ sudo vim /etc/circus/conf.d/wordplease.ini
```

Con el siguiente contenido (recuerda cambiar los datos sensibles):

```
[watcher:wordplease]
working_dir = /home/wordplease/wordplease/src/
cmd = gunicorn
args = -w 1 -t 180 --pythonpath=. -b unix:/home/wordplease/wordplease.sock wordplease.wsgi
uid = wordplease
numprocesses = 1
autostart = true
send_hup = true
stdout_stream.class = FileStream
stdout_stream.filename = /home/wordplease/logs/gunicorn.stdout.log
stdout_stream.max_bytes = 10485760
stdout_stream.backup_count = 4
stderr_stream.class = FileStream
stderr_stream.filename = /home/wordplease/logs/gunicorn.stderr.log
stderr_stream.max_bytes = 10485760
stderr_stream.backup_count = 4
copy_env = true
virtualenv = /home/wordplease/.pyenv/versions/env
virtualenv_py_ver = 3.6

[env:wordplease]
DJANGO_SETTINGS_MODULE = wordplease.settings_production
SECRET_KEY = <secret_key>
DB_NAME = wordplease
DB_USER = wordplease
```

Ahora simplemente iniciamos el servicio de circus y nuestra app
estará en marcha. Para tenerla online, tenemos que configurar
un sitio en el servidor web `nginx`.

```
# /etc/nginx/sites-available/wordplease
server {
	listen 80;
	server_name wordplease.tonygb.com;

	access_log /home/wordplease/logs/nginx-access.log;
	error_log /home/wordplease/logs/nginx-error.log;

	root /home/wordplease/wordplease/src/;

	client_max_body_size 10M;

	location /static {
		alias /home/wordplease/wordplease/src/static;
	}

    location /media {
        alias /home/wordplease/wordplease/src/media;
    }

	location / {
		include proxy_params;
		proxy_pass http://unix:/home/wordplease/wordplease.sock;
	}
}
```

Creando un enlace simbólico en sites-enabled lo tendremos listo.
Obviamente, en el proveedor de dominio hemos establecido el DNS
para acceder a la IP del servidor.

```
$ sudo ln -s /etc/nginx/sites-available/wordplease /etc/nginx/sites-enabled/
```

Probamos la configuración y si todo está correcto reiniciamos
el servicio `nginx`.

```
$ sudo nginx -t
$ sudo service nginx restart
```

# Referencias
Basado en el gist https://gist.github.com/kasappeal/b54ecf22ca302223fa914d3e355c7c21
de Alberto Casero.