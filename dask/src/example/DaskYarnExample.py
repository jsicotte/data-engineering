from dask_yarn import YarnCluster
from dask.distributed import Client, progress, performance_report
import dask.array as da

cluster = YarnCluster(
    environment='/venv.tar.gz',
    worker_memory='1GiB',
    scheduler_memory='1GiB',
    dashboard_address=':45555'
)
client = Client(cluster)
cluster.scale(2)

with performance_report(filename="/test/dask-report.html"):
    x = da.random.random((100, 100), chunks=(100, 100))
    y = x + x.T
    y = y.persist()
    progress(y)

    y.compute()
    print(f"the result is: {y}")