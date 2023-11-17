#!/bin/bash

# Directorio donde se encuentran los shapefiles
SHAPEFILES_DIR="/yafun"

# Datos de conexión a la base de datos
DB_NAME="ruteo"
DB_USER="root"
DB_HOST="localhost"  # Usa 'localhost' si ejecutas el script fuera de Docker
DB_PORT="5432"
DB_PASSWORD="ruteo"  # Asegúrate de cambiar esto por tu contraseña real

echo "Esperando a que la base de datos esté lista..."
#until PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c '\q'; do
#  echo "La base de datos no está lista. Esperando..."
#  sleep 10
#done

echo "La base de datos está lista. Procediendo con la importación de shapefiles."

for shpfile in "$SHAPEFILES_DIR"/*.shp; do
    TABLE_NAME=$(basename "$shpfile" .shp)
    shp2pgsql -I -s 4326 "$shpfile" $TABLE_NAME | PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "ALTER TABLE $TABLE_NAME ADD COLUMN probabilidad_falla DOUBLE PRECISION DEFAULT 0;"
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT pgr_createTopology('$TABLE_NAME', 0.0001, 'geom', 'id');"
done

echo "Importación y creación de topología completadas."

