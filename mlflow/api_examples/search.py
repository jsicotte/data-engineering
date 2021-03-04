import requests
import json
url = 'http://localhost:5000/api/2.0/preview/mlflow/model-versions/search?name=ModelsElasticnetWineModel'
response = requests.get(url=url)
parsed = json.loads(response.content)
current_prod_version = next(v for v in parsed['model_versions'] if v['current_stage'] == 'Production')
print(json.dumps(current_prod_version, indent=4))
