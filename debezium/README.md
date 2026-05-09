# Instructions
First run the services with `docker compose up -d`. Next, initialize the MySQL connector:

```
curl -i -X POST \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
localhost:8083/connectors/ -d '{
    "name": "inventory-connector",
    "config": {
        "connector.class": "io.debezium.connector.mysql.MySqlConnector",
        "tasks.max": "1",
        "database.hostname": "mysql",
        "database.port": "3306",
        "database.user": "root",
        "database.password": "debezium",
        "database.server.id": "184054",
        "topic.prefix": "dbserver1",
        "database.include.list": "inventory",
        "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",
        "schema.history.internal.kafka.topic": "schemahistory.inventory"
    }
}'
```



./bin/spark-submit \                          
    --master k8s://https://127.0.0.1:57132 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=2 \
    --conf "spark.executor.extraJavaOptions=-Djava.security.manager=allow"  \
    --conf spark.kubernetes.container.image=spark:testingjava11 \
    local:///examples/jars/spark-examples_2.12-3.5.5.jar

    ./bin/spark-submit \                          
    --master k8s://https://127.0.0.1:57132 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark
    --conf spark.executor.instances=2 \
    --conf spark.kubernetes.container.image=spark:testingjava11 \
    local:///examples/jars/spark-examples_2.12-3.5.5.jar




./bin/spark-submit  --master k8s://https://127.0.0.1:57132 --deploy-mode cluster   --name spark-pi     --class org.apache.spark.examples.SparkPi    --conf spark.executor.instances=2   --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark  --conf spark.kubernetes.container.image=spark:testingjava17    local:///examples/jars/spark-examples_2.12-3.5.5.jar



./bin/spark-submit --master k8s://https://127.0.0.1:57132 --conf spark.kubernetes.container.image=spark:v3.2.1 --conf spark.kubernetes.context=minikube  --conf spark.kubernetes.namespace=spark-demo  --conf spark.kubernetes.container.image=spark:testingjava11  --verbose



K8S_SERVER=$(kubectl config view --output=jsonpath='{.clusters[].cluster.server}')

./bin/spark-shell \
  --master k8s://http://127.0.0.1:8001  \
  --conf spark.kubernetes.container.image=spark:testingjava17 \
  --conf spark.kubernetes.context=minikube \
  --conf spark.kubernetes.namespace=spark-demo \
  --conf spark.executor.extraJavaOptions="-Djava.security.manager=allow" \
      --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  --verbose


./bin/spark-submit  --master k8s://https://127.0.0.1:57132 --deploy-mode cluster   --name spark-pi     --class org.apache.spark.examples.SparkPi    --conf spark.executor.instances=2   --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark  --conf spark.kubernetes.container.image=spark:la2test --conf spark.kubernetes.authenticate.caCertFile=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt  --conf spark.kubernetes.authenticate.oauthTokenFile=/var/run/secrets/kubernetes.io/serviceaccount/token   local:///examples/jars/spark-examples_2.12-3.5.5.jar

./bin/spark-shell \
  --master k8s://http://127.0.0.1:8001  \
  --conf spark.kubernetes.container.image=sparasdfasfk:testingjasdfasdfava17 \
  --conf spark.kubernetes.context=minikube \
  --conf spark.kubernetes.namespace=spark-demo \
  --conf spark.executor.extraJavaOptions="-Djava.security.manager=allow" \
      --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  --verbose