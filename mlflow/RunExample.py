import mlflow

mlflow.set_experiment("run example2")

with mlflow.start_run():
    mlflow.log_param("a", 1)
    mlflow.log_param("b", 2)

    mlflow.set_tag("test tag", "some value")