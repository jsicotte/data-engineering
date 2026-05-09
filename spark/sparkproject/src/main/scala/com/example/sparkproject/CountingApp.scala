package com.example.sparkProject

import org.apache.spark.sql.types.{IntegerType, StringType, StructField, StructType}
import org.apache.spark.sql.{Row, SparkSession}
import org.apache.spark.{SparkConf, SparkContext}

/**
 * Use this to test the app locally, from sbt:
 * sbt "run inputFile.txt outputFile.txt"
 * (+ select CountingLocalApp when prompted)
 */
object CountingLocalApp extends App {
    val spark = SparkSession.builder()

      .getOrCreate()

    val someData = Seq(Row(8, "bat"))
    val someSchema = List(StructField("number", IntegerType, true), StructField("word", StringType, true))
    val someDF = spark.createDataFrame(spark.sparkContext.parallelize((someData)), StructType(someSchema))
    someDF.write.format("parquet").mode("append").save("test.parquet")
}

/**
 * Use this when submitting the app to a cluster with spark-submit
 * */
object CountingApp extends App {
    //val (inputFile, outputFile) = (args(0), args(1))

    // spark-submit command should supply all necessary config elements
    Runner.run(new SparkConf())
}

object Runner {
    def run(conf: SparkConf): Unit = {
        //val sc = new SparkContext(conf)
        val spark: SparkSession = SparkSession.builder().master("local[1]").appName("test").getOrCreate()
        val rdd = spark.sparkContext.textFile("s3a://test-bucket/README.MD")


        //val rdd = sc.textFile(inputFile)
        val counts = WordCount.withStopWordsFiltered(rdd)
        counts.saveAsTextFile("output.txt")
    }
}
