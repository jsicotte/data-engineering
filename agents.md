# agents.md

This file provides context for AI coding agents working in this repository. Each subdirectory is an independent proof-of-concept (PoC) exploring a specific data engineering technology. They are personal research experiments by Jason Sicotte and are not a single unified application. Read this file first before exploring any subdirectory.

---

## Directory Index

### `airflow/`
**Technology:** Apache Airflow (workflow orchestration)
**Deployment:** Docker Compose
**Summary:** Runs Airflow with the CeleryExecutor using a custom-built image on Ubuntu 18.04 / Python 3.6. Redis acts as the Celery broker and MySQL as the metadata database. A single example DAG (`example_bash_operator.py`) demonstrates task chaining with `BashOperator`.
**Key integrations:** Redis (broker), MySQL (metadata DB)
**Note:** Fernet key is hardcoded — dev/PoC only.

---

### `apache-atlas/`
**Technology:** Apache Atlas 2.1.0 (data governance and metadata management)
**Deployment:** Docker Compose (single container, built from `Dockerfile`)
**Summary:** Deploys Apache Atlas configured to use HBase as its graph storage backend and Solr (SolrCloud) as its graph search index. Embedded Kafka is used for `ATLAS_HOOK` and `ATLAS_ENTITIES` event streaming. Atlas's HTTP server runs on port 2100.
**Key integrations:** HBase + ZooKeeper (from `hadoop/hbase/`), Solr (`solr/`), Elasticsearch (`elasticsearch/`, referenced but commented out in config), shared `custom_network`
**Note:** Depends on the Hadoop HBase and Solr PoCs being up and reachable on `custom_network`.

---

### `apache-druid/`
**Technology:** Apache Druid (real-time analytics database)
**Deployment:** Helm (Kubernetes)
**Summary:** A scaffolded Helm chart for deploying Druid on Kubernetes. The chart templates are generated boilerplate and `values.yaml` still references the default `nginx` image — no actual Druid configuration has been applied.
**Key integrations:** None
**Note:** This is an empty placeholder. The PoC was never implemented.

---

### `bi/`
**Technology:** Cube.js (semantic layer / headless BI framework)
**Deployment:** Kubernetes manifests
**Summary:** Deploys a Cube.js semantic layer on Kubernetes backed by PostgreSQL as a data source, Redis for query caching, and CubeStore for pre-aggregation materialization. The `schema/Orders.js` cube defines measures and dimensions over a small inline dataset, demonstrating the SQL API with authentication.
**Key integrations:** PostgreSQL (data source), Redis (cache), CubeStore (pre-aggregations)
**Note:** SQL API is enabled with MySQL and PostgreSQL wire protocol support (ports 3306/5432).

---

### `common-infrastructure/`
**Technology:** MinIO (S3-compatible object storage) via the MinIO Operator
**Deployment:** Helm (Kubernetes)
**Summary:** Helm values for a production-grade MinIO deployment using the MinIO Operator pattern. Configures an Operator (2 replicas) and a Tenant named `myminio` with 4 servers × 4 volumes × 10Gi — the minimum erasure-coding configuration. This is the Kubernetes-native MinIO deployment intended to back Spark, Iceberg, and MLflow workloads.
**Key integrations:** Prometheus (scrape annotations on the tenant), Spark (`spark/`), Iceberg (`iceburg/`), MLflow (`mlflow/`)
**Note:** Distinct from the simpler `minio/` directory — see cross-cutting concerns below.

---

### `dask/`
**Technology:** Dask (Python parallel computing) on Hadoop YARN
**Deployment:** Docker Compose
**Summary:** Runs Dask distributed computations on a Hadoop YARN cluster. The Dockerfile builds on the `master-image` from `hadoop/hdfs/`, installs `dask[complete]` and `dask-yarn` into a virtualenv, and packages it with `venv-pack` for distribution to YARN workers. An nginx reverse proxy is used to expose the Dask dashboard (which starts on a random port on an arbitrary YARN worker node).
**Key integrations:** Hadoop HDFS + YARN (`hadoop/hdfs/`), nginx (dashboard proxy), JupyterLab (`jupyter/`)
**Note:** The Dask dashboard routing challenge (random port on random worker) is solved via `jupyter-server-proxy` in the `jupyter/` PoC.

---

### `debezium/`
**Technology:** Debezium (Change Data Capture)
**Deployment:** Docker Compose
**Summary:** A CDC pipeline capturing MySQL change events and streaming them to Kafka. Services include ZooKeeper, Kafka, a Debezium-flavored MySQL pre-loaded with an `inventory` database, and Kafka Connect running the Debezium MySQL connector. The README contains the `curl` command to register the connector.
**Key integrations:** MySQL (CDC source), Kafka (event stream destination), ZooKeeper (Kafka coordination)
**Note:** The README also contains unrelated `spark-submit` scratch notes from the Spark-on-Kubernetes PoC.

---

### `elasticsearch/`
**Technology:** Elasticsearch 7.2.0 + Kibana (search and analytics)
**Deployment:** Docker Compose
**Summary:** Runs a single-node Elasticsearch 7.2.0 instance and Kibana on the shared `custom_network`. The compose file also has commented-out entries for Elasticsearch 6.4.1, Amazon OpenDistro variants, and a cAdvisor container for Docker resource monitoring.
**Key integrations:** `custom_network` (consumed by Apache Atlas as an alternative search backend), cAdvisor (container monitoring)
**Note:** The OpenDistro and v6.4.1 entries are commented out. Only the v7.2.0 node is active.

---

### `hadoop/`
**Technology:** Apache Hadoop (HDFS + YARN + HBase + ZooKeeper)
**Deployment:** Docker Compose (two sub-stacks)
**Summary:** The foundational infrastructure layer for this repo. `hadoop/hdfs/` runs a full HDFS + YARN cluster (NameNode, two DataNodes, ResourceManager, two NodeManagers) using Hadoop 2.7.6 on CentOS 7. `hadoop/hbase/` runs a distributed HBase 2.3.1 cluster (Master, two RegionServers, ZooKeeper) on CentOS 6. The `master-image` Docker image built here is the base image for `dask/` and `jupyter/`.
**Key integrations:** Base image for `dask/` and `jupyter/`; ZooKeeper used by `apache-atlas/`, `solr/`, and `hadoop/hbase/`; YARN used by `dask/` and `spark/`; HBase used by `apache-atlas/`
**Note:** There is a minor syntax error in `hadoop/hbase/docker-compose.yaml` (`start"]` should be `"start"`).

---

### `iceburg/`
**Technology:** Apache Iceberg (open table format) with Spark, MinIO, and Apache Polaris
**Deployment:** Docker Compose (main stack) + Polaris source checkout
**Summary:** Runs a Spark + Iceberg environment with JupyterLab (port 8888), an Iceberg REST catalog server (port 8181), and a standalone MinIO instance as the S3 warehouse backend (`s3://warehouse/`). A MinIO Client init container creates the warehouse bucket on startup. The `polaris/` subdirectory contains a full checkout of the Apache Polaris (incubating) source — an alternative open-source Iceberg REST catalog — which was explored as a replacement for the `iceberg-rest-fixture`.
**Key integrations:** MinIO (warehouse storage), Iceberg REST catalog, Spark (query engine), Apache Polaris (catalog alternative)
**Note:** The JupyterLab notebooks directory is empty — no notebooks have been committed. Note the directory name is spelled `iceburg` (not `iceberg`).

---

### `jupyter/`
**Technology:** JupyterLab, nteract, Jupyter Commuter (notebook environments)
**Deployment:** Docker Compose
**Summary:** A multi-interface notebook environment layered on top of the Dask + Hadoop stack. The primary `jupyter-hadoop` service builds on the `dask/` image and configures `HADOOP_HOME`, `SPARK_HOME`, `HADOOP_CONF_DIR`, and `YARN_CONF_DIR`. It installs `dask-labextension` and `jupyter-server-proxy` to tunnel Dask dashboard URLs (running on random YARN worker ports) through JupyterLab's URL space. nteract (port 8889) and Jupyter Commuter (port 4000) are also available.
**Key integrations:** Dask (`dask/`), Hadoop YARN (`hadoop/hdfs/`), Spark (SPARK_HOME configured), `custom_network`
**Note:** `jupyter-server-proxy` with a host whitelist is the key design decision — it solves the Dask-on-YARN dashboard routing problem described in both the `dask/` and `jupyter/` READMEs.

---

### `marimo_notebooks/`
**Technology:** Marimo (reactive Python notebook framework)
**Deployment:** Local (`uv` virtual environment, Python 3.12+)
**Summary:** A local Marimo project with two notebooks: `example_notebook.py` demonstrates reactive UI (slider), Markdown rendering, and a DuckDB + Pandas DataFrame example; `polars_examples.py` introduces Polars DataFrames with `.glimpse()` and `.schema`. Unlike the other directories, this has no Docker, no Kubernetes, and no connection to the shared infrastructure.
**Key integrations:** DuckDB (inline queries), Polars (DataFrames), Pandas
**Note:** This is the most modern and self-contained PoC in the repo. Managed entirely with `uv`.

---

### `minio/`
**Technology:** MinIO (standalone S3-compatible object storage)
**Deployment:** Docker Compose
**Summary:** A minimal single-container MinIO instance on `custom_network`, serving the S3-compatible API on port 9000. This is the simpler, Docker Compose-based MinIO deployment used alongside the other `custom_network` services (Atlas, MLflow, Spark history server).
**Key integrations:** `custom_network` (consumed by Apache Atlas, MLflow, Spark), same S3 credentials reused in `mlflow/docker-compose.yaml`
**Note:** Distinct from `common-infrastructure/minio/`, which is the Kubernetes Operator-based deployment. See cross-cutting concerns below.

---

### `mlflow/`
**Technology:** MLflow (ML experiment tracking and model registry)
**Deployment:** Docker Compose
**Summary:** A complete MLflow tracking environment with MySQL as the backend metadata store and MinIO as the S3-compatible artifact store (`s3://my-mlflow-bucket/`). Includes training scripts for an ElasticNet model on the UCI Wine Quality dataset (`train.py`, `Example.py`), nested run examples, and an `MLproject` file for reproducible `mlflow run` execution inside the Docker network. Model registration and serving are demonstrated in the README.
**Key integrations:** MySQL (metadata backend), MinIO (artifact storage), scikit-learn (model training), MLflow Projects (Docker-based reproducible runs)
**Note:** `Example.py` patches boto3 to redirect S3 calls to the local MinIO endpoint — required for the artifact store to work locally.

---

### `prometheus/`
**Technology:** Prometheus + Grafana (metrics collection and visualization)
**Deployment:** Docker Compose
**Summary:** A minimal two-service monitoring skeleton: Prometheus 2.1.0 (port 9090) and Grafana 7.0.5 (port 3000). No custom `prometheus.yml` scrape configuration is present, so no targets are configured. The services don't have a network block defined.
**Key integrations:** Referenced by the MinIO tenant manifest in `spark/` (Prometheus scrape annotations); intended to monitor the broader ecosystem
**Note:** This PoC is incomplete — it is a bare skeleton with no scrape targets or dashboards configured.

---

### `python/`
**Technology:** Python
**Deployment:** N/A
**Summary:** Empty directory. No files committed.
**Note:** Placeholder only.

---

### `solr/`
**Technology:** Apache Solr 8.6.3 (search platform)
**Deployment:** Docker Compose (single container, built from `Dockerfile`)
**Summary:** Runs Solr in SolrCloud mode (port 8984), connecting to the ZooKeeper service from the HBase cluster on `custom_network`. Includes a custom Solr core configuration (`schema.xml`, `solrconfig.xml`). Its sole purpose in this repo is to serve as the graph index search backend for Apache Atlas.
**Key integrations:** ZooKeeper (`hadoop/hbase/`), Apache Atlas (`apache-atlas/`), `custom_network`
**Note:** Tightly coupled to the Atlas PoC — it is not useful in isolation without Atlas running.

---

### `spark/`
**Technology:** Apache Spark (distributed data processing)
**Deployment:** Docker Compose (YARN mode, older) + Kubernetes (newer)
**Summary:** A multi-generational Spark PoC. The older Docker Compose setup runs a Spark 2.4.0 History Server reading event logs from HDFS. The newer Kubernetes setup builds a Spark 3.5.5 image with Hadoop 3 / S3A support and includes RBAC manifests, a MinIO tenant manifest, and a Scala SBT project (`sparkproject/`) with word count and S3A read examples. The README contains `spark-submit` scratch notes for minikube.
**Key integrations:** HDFS + YARN (`hadoop/hdfs/`) for the older stack; MinIO/S3A (`common-infrastructure/`) and Kubernetes for the newer stack; `hadoop-aws` library for S3A filesystem
**Note:** `spark-3.5.5-bin-hadoop3.tgz` is committed directly to the repo. The Scala project targets Spark 3.5.1, Scala 2.13, Java 17.

---

### `superset/`
**Technology:** Apache Superset (data visualization and BI)
**Deployment:** Helm (Kubernetes)
**Summary:** Helm `values.yaml` for deploying Apache Superset on Kubernetes. Configures Superset web nodes, Celery workers, PostgreSQL (Bitnami chart) as the metadata store, and Redis as the Celery broker and cache. The bootstrap script pre-installs `elasticsearch-dbapi` and `sqlalchemy-bigquery` connectors, and a Mapbox API key is configured for geographic visualizations.
**Key integrations:** PostgreSQL (metadata), Redis (Celery), Elasticsearch (`elasticsearch/`), BigQuery (external datasource), Mapbox (geo charts)
**Note:** `loadExamples: false`. Admin credentials default to `admin`/`admin`.

---

## Cross-Cutting Concerns

### Shared Docker Network (`custom_network`)

Most Docker Compose-based PoCs declare an external network named `custom_network` (also referred to as `proxynet` or `my-proxy-net` in some compose files). This means the following services are designed to communicate with each other when running simultaneously:

- `hadoop/hdfs/` (HDFS, YARN, NameNode)
- `hadoop/hbase/` (HBase, ZooKeeper)
- `solr/` (SolrCloud)
- `apache-atlas/` (Atlas server)
- `elasticsearch/` (Elasticsearch, Kibana)
- `minio/` (MinIO S3)
- `airflow/` (Airflow, Redis, MySQL)
- `spark/` (Spark History Server)
- `jupyter/` (JupyterLab)
- `dask/` (Dask + nginx)

When working on any of these PoCs, be aware that service hostnames (e.g., `zookeeper`, `node-master`, `kafka`) are DNS names on this shared network — not `localhost`.

### Dependency Stack

The PoCs have a clear dependency hierarchy:

```
hadoop/hdfs/          <- foundational; provides HDFS, YARN, and the master-image Docker base
  └─ hadoop/hbase/    <- adds ZooKeeper + HBase (required by Atlas and Solr)
       └─ solr/       <- SolrCloud for Atlas graph indexing (requires ZooKeeper)
            └─ apache-atlas/  <- requires HBase (storage) + Solr (index) + ZooKeeper
  └─ dask/            <- builds on master-image; runs Dask on YARN
       └─ jupyter/    <- builds on dask image; JupyterLab with Hadoop/YARN/Spark env
minio/                <- S3 storage for mlflow/ and older spark/ setup
  └─ mlflow/          <- uses minio + mysql for tracking + artifact storage
common-infrastructure/minio/  <- K8s MinIO Operator (backs spark/ K8s and iceburg/)
  └─ spark/ (K8s)     <- reads/writes via S3A to MinIO
  └─ iceburg/         <- Iceberg REST catalog + Spark uses MinIO as warehouse
```

`bi/`, `superset/`, `debezium/`, `prometheus/`, `marimo_notebooks/`, and `apache-druid/` are self-contained and do not depend on other directories.

### Deployment Evolution

There is a visible shift from older to newer deployment patterns across the repo:

| Older generation | Newer generation |
|---|---|
| Docker Compose | Kubernetes / Helm |
| Hadoop 2.7.6, Spark 2.4.0 | Spark 3.5.5, Java 17 |
| CentOS 6 / CentOS 7 | UBI 9 / modern base images |
| YARN as cluster manager | Kubernetes as cluster manager |
| Python 3.6–3.7 | Python 3.12+, `uv`, Marimo |
| `minio/` (standalone) | `common-infrastructure/minio/` (Operator) |

When modifying or extending a PoC, check which generation it belongs to before assuming consistent tooling or base images.

### Two MinIO Deployments

There are two separate MinIO setups in this repo with different purposes:

- **`minio/`** — Simple standalone MinIO container on `custom_network`. Used by `mlflow/` and older Docker Compose-based services. Credentials: `AKIAIOSFODNN7EXAMPLE` / `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`.
- **`common-infrastructure/minio/`** — MinIO Operator + Tenant on Kubernetes. Used by `spark/` (Kubernetes mode) and `iceburg/`. Production-grade erasure-coded setup (4 servers × 4 volumes).

Do not conflate these two — they serve different stacks and have different access patterns.
