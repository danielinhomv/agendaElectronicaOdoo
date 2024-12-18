# Imagen base de Odoo 17
FROM odoo:17

# Configurar variables de entorno
ENV DEBIAN_FRONTEND=noninteractive

# Directorio de trabajo
WORKDIR /mnt/extra-addons

# Copiar tus archivos personalizados (módulos y configuraciones)
COPY . /mnt/extra-addons

# Instalar dependencias requeridas de Python
RUN pip install --no-cache-dir PyJWT cloudinary firebase-admin

# Exponer el puerto de Odoo
EXPOSE 8069

# Comando por defecto para ejecutar el servidor Odoo
CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
