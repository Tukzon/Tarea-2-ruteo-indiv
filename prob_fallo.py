import psycopg2

conn_params = {
    'dbname': 'ruteo',
    'user': 'postgres',
    'password': 'ruteo',
    'host': 'localhost',
    'port': '5432'
}

conn = psycopg2.connect(**conn_params)
cur = conn.cursor()

cur.execute("SELECT ST_X(wkb_geometry) as lon, ST_Y(wkb_geometry) as lat FROM \"88\" WHERE ogc_fid = 1")
epicentro = cur.fetchone()
epicentro_lon, epicentro_lat = epicentro

lambda_param = 500

cur.execute("""
    UPDATE fibra_optica
    SET probabilidad_fallo = EXP(-ST_Distance(geom::geography, ST_MakePoint(%s, %s)::geography) / 1000 / %s)
    WHERE ST_Distance(geom::geography, ST_MakePoint(%s, %s)::geography) IS NOT NULL
""", (epicentro_lon, epicentro_lat, lambda_param, epicentro_lon, epicentro_lat))

conn.commit()
cur.close()
conn.close()

print("La actualización de la probabilidad de fallo ha finalizado.")