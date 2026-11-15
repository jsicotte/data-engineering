# python-example

Minimal `uv`/PyIceberg project: builds a PyArrow table and persists it as an
Iceberg table via the Apache Polaris REST catalog from `../docker-compose.yaml`,
backed by RustFS (S3-compatible storage).

Python/[PyIceberg](https://pypi.org/project/pyiceberg/) counterpart to
`../spark-example` (Scala/Spark).

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/)
- The Polaris/RustFS stack running: `docker compose up -d` from `..`

## Run

```sh
cd ..
docker compose up -d
cd python-example
uv run python-example
```

This creates namespace `hello_world` and table `people` in the
`quickstart_catalog` catalog, writes 3 rows (dropping/recreating the table
first, like `createOrReplace`), then reads them back and prints the result.

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

## Notes

- The REST catalog's default `X-Iceberg-Access-Delegation: vended-credentials`
  header is explicitly disabled (`header.X-Iceberg-Access-Delegation: ""`):
  the bootstrapped Polaris `root` principal isn't granted the
  `CREATE_TABLE_DIRECT_WITH_WRITE_DELEGATION` privilege, so the client falls
  back to direct writes using the static S3 credentials above — matching
  what the Scala/Spark example does.
