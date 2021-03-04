import mlflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("run example")

with mlflow.start_run(run_name="some experiment"):
    mlflow.log_param("a", 1)
    mlflow.log_param("b", 2)

    mlflow.set_tag("test tag", "some run")

    with mlflow.start_run(nested=True, run_name="run name"):
        mlflow.log_param("c", 2)
