"""Minimal Iceberg "hello world": creates a PyArrow table and persists it as
an Iceberg table in Apache Polaris, backed by RustFS (S3-compatible storage).

Requires the Polaris + RustFS stack from ../docker-compose.yaml to be
running (`docker compose up -d`).

Python/PyIceberg counterpart to ../../spark-example (Scala/Spark).
"""

from __future__ import annotations

import os

import pyarrow as pa
from pyiceberg.catalog import load_catalog


def main() -> None:
    catalog_name = os.environ.get("CATALOG_NAME", "quickstart_catalog")
    polaris_uri = os.environ.get("POLARIS_URI", "http://localhost:8181/api/catalog")
    client_id = os.environ.get("POLARIS_CLIENT_ID", "root")
    client_secret = os.environ.get("POLARIS_CLIENT_SECRET", "s3cr3t")
    s3_endpoint = os.environ.get("S3_ENDPOINT", "http://localhost:9000")
    s3_access_key = os.environ.get("AWS_ACCESS_KEY_ID", "polaris_root")
    s3_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "polaris_pass")

    catalog = load_catalog(
        "polaris",
        **{
            "type": "rest",
            "uri": polaris_uri,
            "warehouse": catalog_name,
            "credential": f"{client_id}:{client_secret}",
            "scope": "PRINCIPAL_ROLE:ALL",
            "s3.endpoint": s3_endpoint,
            "s3.access-key-id": s3_access_key,
            "s3.secret-access-key": s3_secret_key,
            "s3.region": "us-west-2",
            # Polaris grants root the catalog-admin role but not the
            # separate "write delegation" (vended-credentials) privilege;
            # disable it and fall back to direct writes using the static
            # S3 credentials above, like the Scala/Spark example does.
            "header.X-Iceberg-Access-Delegation": "",
        },
    )

    namespace = "hello_world"
    table_identifier = f"{namespace}.people"

    catalog.create_namespace_if_not_exists(namespace)

    arrow_table = pa.table(
        {
            "id": pa.array([1, 2, 3], type=pa.int32()),
            "name": ["alice", "bob", "carol"],
            "age": pa.array([34, 29, 41], type=pa.int32()),
        }
    )

    if catalog.table_exists(table_identifier):
        catalog.drop_table(table_identifier)
    table = catalog.create_table(table_identifier, schema=arrow_table.schema)
    table.append(arrow_table)

    print(f"Wrote table polaris.{table_identifier}. Reading it back:")
    result = table.scan().to_arrow().sort_by("id")
    for row in result.to_pylist():
        print(row)


if __name__ == "__main__":
    main()
