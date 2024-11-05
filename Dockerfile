# Usa la imagen base de Odoo
FROM odoo:17

# Copia los archivos de configuración
# COPY ./config/odoo.conf /etc/odoo/odoo.conf

# Copia los addons personalizados
# COPY ./addons /mnt/extra-addons

# Copia el archivo de inicialización
COPY ./init.sh /docker-entrypoint-init.d/init.sh

# Haz que el archivo de inicialización sea ejecutable
USER root
RUN chmod +x /docker-entrypoint-init.d/init.sh

# Vuelve al usuario odoo
USER odoo

# Establece el punto de entrada predeterminado
# CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
