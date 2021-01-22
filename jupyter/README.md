# Jupyter Lab Example
This configuration can be used both with Spark and Dask using Hadoop Yarn.
## Launch Order
The base image for the Jupyter container is based off the the container that is built in the dask directory.
## Notes About Dask
When running in Yarn Dask picks a worker picks an arbitrary worker node and starts the dashboard on a random port. To
get around this issue the Jupyter Lab Proxy extension is used. The proxying to the worker nodes is configured with two files:
* jupyter_lab_config.py: This file contains the whitelist for hosts to connect to. The proxy extension does not allow for connections to arbitrary hosts and ports, so this must be configured.
* config.yaml: This is a Dask configuration file that reconfigures the dashboard URLs to be conform to the proxying url format: {jupyter base url}/proxy/{host with dashboard}:{random port it picked}.
# Useful Links
[host_whitelist Example](https://github.com/jupyterhub/jupyter-server-proxy/blob/master/jupyter_server_proxy/config.py) This has some helpful comments on how to use the setting.
[Jupyter Server Proxy](https://jupyter-server-proxy.readthedocs.io/en/latest/server-process.html) This has some additional info on how to configure the proxy with a .py file. I may end up using a callable that just returns true for the whitelist in a future version. That sort of practice would not be secure for production use but will make
setup easier.
[Stackoverflow Qustion](https://stackoverflow.com/a/64877932) This is where I first saw some code that shows how to configure the whitelist. The documentation on the Server Proxy website does not actually tell you how to configure this.
[Jupyter Configuration](https://jupyter.readthedocs.io/en/latest/use/jupyter-directories.html#config-dir) I can never remember where the configuration files are so this page helps.
[Distributed Dask Configuration Parameters](https://docs.dask.org/en/latest/configuration-reference.html#dashboard) Just a simple list for reference.
[Dask Config Locations](https://docs.dask.org/en/latest/configuration.html) Helpful because you need to know where to put the parameters above.
[Server Proxy Install](https://jupyter-server-proxy.readthedocs.io/en/latest/install.html) How to install the proxy extension.
# TODO
- copy the python environment to hdfs so it does not need to be stored in the image.