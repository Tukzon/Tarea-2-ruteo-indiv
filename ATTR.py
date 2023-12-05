import psycopg2
import itertools

conn_params = {
    'dbname': 'ruteo',
    'user': 'postgres',
    'password': 'ruteo',
    'host': 'localhost',
    'port': '5432'
}

conn = psycopg2.connect(**conn_params)
cur = conn.cursor()

cur.execute("""
    SELECT node, component
    FROM pgr_connectedComponents(
        'SELECT gid AS id, source, target, 1::FLOAT8 AS cost FROM fibra_optica'
    )
""")
componentes = cur.fetchall()

nodos_por_componente = {}
for nodo, componente in componentes:
    if componente not in nodos_por_componente:
        nodos_por_componente[componente] = []
    nodos_por_componente[componente].append(nodo)

def calcular_conectividad_operativa(s, d):
    try:
        cur.execute("""
            SELECT * FROM pgr_dijkstra(
                'SELECT gid AS id, source, target, 1 - probabilidad_fallo AS cost FROM fibra_optica',
                %s, %s, directed := false
            );
        """, (s, d))
        ruta = cur.fetchall()
        probabilidad_ruta_operativa = 1
        for segmento in ruta:
            edge_id = segmento[2]
            if edge_id > -1:
                cur.execute("""
                    SELECT 1 - probabilidad_fallo FROM fibra_optica WHERE gid = %s;
                """, (edge_id,))
                resultado = cur.fetchone()
                if resultado is not None:
                    probabilidad_ruta_operativa *= resultado[0]
                else:
                    probabilidad_ruta_operativa = 0
                    break
        return probabilidad_ruta_operativa
    except psycopg2.Error as e:
        conn.rollback()
        return 0 

suma_conectividad_total = 0
total_pares_total = 0
for nodos_componente in nodos_por_componente.values():
    conectividad_componente = 0
    total_pares_componente = len(nodos_componente) * (len(nodos_componente) - 1) // 2
    if total_pares_componente > 0:
        for s, d in itertools.combinations(nodos_componente, 2):
            conectividad_componente += calcular_conectividad_operativa(s, d)
    suma_conectividad_total += conectividad_componente
    total_pares_total += total_pares_componente

attr = suma_conectividad_total / total_pares_total if total_pares_total > 0 else 0

print(f"El Average Two-Terminal Reliability (ATTR) es: {attr}")

cur.close()
conn.close()