# Starting the MLFlow Example
Docker Compose can be used to start the MLFlow UI with MinIO and MySQL: `docker-compose up -d`.

# Run the Training
To create the model run: `mlflow run -A network=mlflow_default .`. It is important to note that this requires that
the MLFLow tracking UI has already been started with Docker Compose.


# Serve Models
To serve a model with the builtin server first export:
```
export MLFLOW_TRACKING_URI=http://localhost:9000/
export MLFLOW_S3_ENDPOINT_URL=http://localhost:9000/
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```
Then run the command: `mlflow models serve --no-conda -m s3://my-mlflow-bucket`.

