# Módulo Administración Academica en Odoo 17 con Docker
### Requisitos
* Tener instalado docker y docker-compose

### Pasos
### 1. Clonar el Repositorio
* Para clonar el repositorio, debes ejecutar:
~~~~
git clone https://github.com/benjamincondori/parcial-software.git
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

~~~~
http://localhost:8069
~~~~