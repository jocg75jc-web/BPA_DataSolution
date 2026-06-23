# Bases de Datos y Repositorios de Almacenamiento mas usados (2026)

## 1. Proposito
Documento de referencia para disenar nuevos procesos con fuentes y destinos alineados al mercado actual.

## 2. Bases de datos mas usadas actualmente

### 2.1 Relacionales transaccionales (OLTP)
- PostgreSQL
- MySQL
- Microsoft SQL Server
- Oracle Database
- SQLite (uso embebido o edge)

### 2.2 Data warehouse / analitica
- Snowflake
- Google BigQuery
- Amazon Redshift
- Azure Synapse Analytics
- Databricks SQL Warehouse

### 2.3 NoSQL y especializadas
- MongoDB (documental)
- Redis (cache y datos en memoria)
- Apache Cassandra (wide-column, alta escala)
- Amazon DynamoDB (NoSQL administrada)
- Elasticsearch / OpenSearch (busqueda y observabilidad)
- Neo4j (grafos)

## 3. Destinos de almacenamiento mas usados

### 3.1 Object storage cloud
- Azure Blob Storage
- Azure Data Lake Storage Gen2
- Amazon S3
- Google Cloud Storage

### 3.2 Repositorios empresariales y transferencia
- SFTP administrado
- SharePoint Online
- OneDrive for Business
- File shares SMB/NFS

### 3.3 Patrones de lakehouse y archivos
- Delta Lake
- Apache Iceberg
- Apache Hudi
- Formatos comunes: Parquet, CSV, JSON

## 4. Recomendacion de seleccion de fuente
1. Si el origen es operacional tradicional:
- Priorizar conector SQL estandar (PostgreSQL/MySQL/SQL Server/Oracle).

2. Si el origen es analitico masivo:
- Priorizar conectores de warehouse (Snowflake/BigQuery/Redshift/Synapse).

3. Si el origen es semiestructurado o eventos:
- Evaluar NoSQL o bus de eventos con etapa de normalizacion.

## 5. Recomendacion de seleccion de destino
1. Si se requiere consumo por BI/ML:
- Priorizar ADLS Gen2, S3 o GCS con Parquet.

2. Si se requiere intercambio B2B o legado:
- Priorizar SFTP con convencion de nombres estricta.

3. Si se requiere colaboracion de negocio:
- Priorizar SharePoint/OneDrive con controles de permisos.

## 6. Matriz origen-destino recomendada
- PostgreSQL/MySQL/SQL Server/Oracle -> ADLS/S3/GCS (Parquet o CSV).
- Snowflake/BigQuery/Redshift/Synapse -> ADLS/S3/GCS (Parquet).
- MongoDB/Cassandra/DynamoDB -> Data lake (JSON/Parquet) + curacion posterior.
- Cualquier origen -> SFTP cuando exista dependencia externa de intercambio.

## 7. Consideraciones tecnicas obligatorias
- Driver/SDK oficial por motor.
- Timeout, retry y circuit-breaker para fallos transitorios.
- Manejo de secretos por entorno.
- Trazabilidad por ejecucion.
- Esquema de versionado para cambios en estructura de salida.

## 8. Checklist rapido para nuevos conectores
- Existe driver estable y soportado.
- Existe estrategia de autenticacion segura.
- Existe prueba de lectura incremental.
- Existe ruta de salida aprobada por seguridad y negocio.
- Existe monitoreo y alertamiento integrado.
