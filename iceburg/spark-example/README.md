# spark-example

Minimal Gradle/Scala Spark project: builds a DataFrame and persists it as an
Iceberg table via the Apache Polaris REST catalog from `../docker-compose.yaml`,
backed by RustFS (S3-compatible storage).

## Prerequisites

- Java 17 (`sdk install java 17.0.14-tem && sdk use java 17.0.14-tem`)
- The Polaris/RustFS stack running: `docker compose up -d` from `..`

## Run

```sh
cd ..
docker compose up -d
cd spark-example
./gradlew run
```

This creates namespace `hello_world` and table `people` in the
`quickstart_catalog` catalog, writes 3 rows, then reads them back and prints
the result.

## Configuration

Overridable via environment variables (defaults match the root
`docker-compose.yaml`):

| Variable | Default |
| --- | --- |
| `CATALOG_NAME` | `quickstart_catalog` |
| `POLARIS_URI` | `http://localhost:8181/api/catalog` |
| `POLARIS_CLIENT_ID` | `root` |
| `POLARIS_CLIENT_SECRET` | `s3cr3t` |
| `S3_ENDPOINT` | `http://localhost:9000` |
| `AWS_ACCESS_KEY_ID` | `polaris_root` |
| `AWS_SECRET_ACCESS_KEY` | `polaris_pass` |
