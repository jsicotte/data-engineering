package com.example.sparkexample

import org.apache.spark.sql.SparkSession

/** Minimal Iceberg "hello world": creates a DataFrame and persists it as an
  * Iceberg table in Apache Polaris, backed by RustFS (S3-compatible storage).
  *
  * Requires the Polaris + RustFS stack from ../docker-compose.yaml to be
  * running (`docker compose up -d`).
  */
object IcebergHelloWorld {

  def main(args: Array[String]): Unit = {
    val catalogName = sys.env.getOrElse("CATALOG_NAME", "quickstart_catalog")
    val polarisUri = sys.env.getOrElse("POLARIS_URI", "http://localhost:8181/api/catalog")
    val clientId = sys.env.getOrElse("POLARIS_CLIENT_ID", "root")
    val clientSecret = sys.env.getOrElse("POLARIS_CLIENT_SECRET", "s3cr3t")
    val s3Endpoint = sys.env.getOrElse("S3_ENDPOINT", "http://localhost:9000")
    val s3AccessKey = sys.env.getOrElse("AWS_ACCESS_KEY_ID", "polaris_root")
    val s3SecretKey = sys.env.getOrElse("AWS_SECRET_ACCESS_KEY", "polaris_pass")

    val spark = SparkSession.builder()
      .appName("iceberg-hello-world")
      .master("local[*]")
      .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
      .config("spark.sql.catalog.polaris", "org.apache.iceberg.spark.SparkCatalog")
      .config("spark.sql.catalog.polaris.type", "rest")
      .config("spark.sql.catalog.polaris.uri", polarisUri)
      .config("spark.sql.catalog.polaris.warehouse", catalogName)
      .config("spark.sql.catalog.polaris.credential", s"$clientId:$clientSecret")
      .config("spark.sql.catalog.polaris.scope", "PRINCIPAL_ROLE:ALL")
      .config("spark.sql.catalog.polaris.io-impl", "org.apache.iceberg.aws.s3.S3FileIO")
      .config("spark.sql.catalog.polaris.s3.endpoint", s3Endpoint)
      .config("spark.sql.catalog.polaris.s3.path-style-access", "true")
      .config("spark.sql.catalog.polaris.client.region", "us-west-2")
      .config("spark.sql.catalog.polaris.s3.access-key-id", s3AccessKey)
      .config("spark.sql.catalog.polaris.s3.secret-access-key", s3SecretKey)
      .config("spark.sql.defaultCatalog", "polaris")
      .getOrCreate()

    import spark.implicits._

    spark.sql(s"CREATE NAMESPACE IF NOT EXISTS polaris.hello_world")

    val df = Seq(
      (1, "alice", 34),
      (2, "bob", 29),
      (3, "carol", 41)
    ).toDF("id", "name", "age")

    df.writeTo("polaris.hello_world.people").createOrReplace()

    println("Wrote table polaris.hello_world.people. Reading it back:")
    spark.table("polaris.hello_world.people").orderBy("id").show()

    spark.stop()
  }
}
