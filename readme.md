# Módulo Administración Academica en Odoo 17 con Docker
### Requisitos
* Tener instalado docker y docker-compose

### Pasos
### 1. Clonar el Repositorio
* Para clonar el repositorio, debes ejecutar:
~~~~
git clone https://github.com/benjamincondori/Administracion-Academica-Odoo.git
~~~~

### 2. Duplicar y renombrar: 
* Duplicar `.env.example` y renombrar la copia con el nombre `.env`
* Duplicar `firebase-admin.example.json` y renombrar la copia con el nombre `firebase-admin.json` y configura las credenciales de tu proyecto de Firebase
* Duplicar `odoo-server.example.log` y renombrar la copia con el nombre `odoo-server.log`

Es importante no editar ni renombrar los archivos que contengan el nombre la palabra example, ya que estos forman parte de tu plantilla.
    
### 3. Establece los parámetros de tu instancia en el archivo `.env`

### 4. Establece los parámetros de tu instancia en el archivo config/odoo.conf
* los parámetros DB_HOST,DB_PASSWD y DB_USER, se establecen en .env. Estos tambien se configuran en el archivo odoo.conf 
* Si estas en producción el parámetro ADMIN_PASSWD de odoo.conf debe ser uno seguro, ya que con este parámetro se gestionan las base de datos.
    
### 5. Ejecución con docker-compose
En la misma raiz del proyecto donde se encuentra docker-compose.yaml, debes ejecutar:
* La primera vez descargará las imagenes de odoo y postgres, esto puede demorar varios minutos.
* Las siguientes ejecuciones deberá demorar solo segundos para iniciarse.

~~~~
docker-compose up -d
~~~~
    
### 6. Instalar paquetes necesarios de python en el contedor de Odoo
* Para ingresar al contendor de odoo, debes ejecutar:

~~~~
docker exec -it odoo_school bash
pip install PyJWT
pip install cloudinary
pip install firebase-admin

~~~~

* Para instalar los paquetes, debes ejecutar:

~~~~
pip install PyJWT
~~~~
~~~~
pip install cloudinary
~~~~
~~~~
pip install firebase-admin
~~~~

* Para salir del contenedor de Odoo, debes ejecutar:

~~~~
exit
~~~~

### 7. Reiniciar el contedor de Odoo
* Para reiniciar el contendor de odoo, debes ejecutar:

~~~~
docker restart odoo_school
~~~~
    
### 8. Acceder a Odoo
* Una vez que los contenedores estén en funcionamiento, puedes acceder a Odoo a través de la siguiente URL:
### 8. Acceder a la db 

docker exec -it odoo_school_db psql -U odoo
\l listar base de datos
\c "nombre de la base de datos" conectarte a una base de datos
\dt listar las tablas de la base de datos
~~~~
http://localhost:8069
~~~~
### 8. en ubuntu
systemctl status docker
cd administracion_academica
ls -a
cp .env.example .env
cd addons/administracion_academica

nano firebase-admin.example
rm -i firebase-admin.example


docker build -t odoo-academico .

sudo apt update

sudo apt install docker-compose


docker-compose up -d    ----si utilizas docker composer.yaml
 
docker run -d -p 8069:8069 --name odoo-academico-container odoo-academico --si no utilizas docker composer.yaml


---vajar desde docker hub-----
cd ~  # (u otro directorio de tu elección)

# Iniciar sesión en Docker Hub (si es necesario)
docker login

# Descargar la imagen desde Docker Hub
docker pull nombre_usuario/odoo-academico:latest

# Verificar que la imagen esté en tu máquina
docker images

# Ejecutar el contenedor de Odoo 
docker run -d -p 8069:8069 --name odoo-academico-container nombre_usuario/odoo-academico:latest
Estos son los pasos para descargar la imagen de Docker desde Docker Hub y ejecutarla. 
Si tienes un archivo docker-compose.yml adecuado, también puedes usar
 docker-compose up -d en su lugar para simplificar el proceso.


---eliminar imagenes---
primero detener los contenedores:docker stop $(docker ps -a -q)
luego eliminar los contenedores : docker rm $(docker ps -a -q)
luego eliminar las imagenes :docker rmi -f 3c84adb64635
luego verifica si existen imagenes : docker images


---subir imagen a docker hub----
1- crea la imagen 
2- agrega etiqueta :docker tag <imagen_local> <usuario_docker_hub>/<nombre_repo>:<tag>
3-sube : docker push danielinho/odoo-academico:latest
//latest es el nombre de la etiqueta , es el nombre de la imagen en tu el repositorio

--vajar la imagen en ubuntu--
1. docker login
2. docker pull <usuario/repositorio:nombre de tu etiqueta o nombre que aparece en el tag en docker hub>
3. ejecutar con docker-compose up -d en caso que tengas contenedores dentro


----bd---
psql -h db -U odoo -d postgres
docker-compose up -d --build (el mas confiable crea la imagen desde cero con el dockerfile)
