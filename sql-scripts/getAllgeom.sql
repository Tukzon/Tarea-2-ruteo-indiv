SELECT geom FROM camino_sin_postacion_detectado cspd
UNION ALL
SELECT geom FROM fibra_optica_detectada fod
union all
select geom from postacion_electrica_detectada ped 
union all
select geom from trayecto_en_ferry tef;