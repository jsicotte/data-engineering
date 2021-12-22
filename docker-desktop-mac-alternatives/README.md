# Docker Desktop Mac Alternative
Since the licensing of Docker Desktop Mac has changed recently, there has been some interest in possible alternatives. Below is a possible list of alternatives.
The replacements are biased for my use cases: docker compse for basic prototype work and Kubernetes for prodution work.

## How To Use My Setup
Install Vagrant and also the 

## Investigation History
### Failed Attempt: lima-vm and nerdcl
At first I looked into using docker-machine since that is what I used prior to the Docker Desktop Mac, however maintenance stopped in 2019 and the project is now dead. Similarly, [boot2docker](https://github.com/boot2docker/boot2docker) is dead as well.

The next step was to look for a docker-machine alternative. This led me to [lima-vm](https://github.com/lima-vm/lima) which is a tool for setting Linux VMs on MacOS. Using this in conjuntion with a "drop in replacement for docker" [nerdctl](https://github.com/containerd/nerdctl), seemed like an option. However its version of compose `nerdctl compose up` is lacking too many features to be an easy replacement for `docker compose`.

### Mostly Functional: Podman
Moving on, I ran accross Podman. There used to be a `podman-machine` but it has since been deprecated and the docs essentially say "just use vagrant". [This article](https://marcusnoble.co.uk/2021-09-01-migrating-from-docker-to-podman/) on the topic of replacing Docker Mac with Podman is a great starting point.

#### Guest vs Host Filesystems
The first step was to create a VM with Vagrant and see if I can run a docker compose file. My initial Vagrantfile looked something like
```
$install = <<-SCRIPT
sudo apt update
sudo apt install -y zsh
sudo apt install -y git
sudo apt install -y podman
SCRIPT

Vagrant.configure("2") do |config|
    config.vm.box = "debian/bullseye64"
    config.vm.provision "shell", inline: $install
end
```
I could run `podman compose up` from the MacOS host, but podman only has access to the filesystem of the Linux guest. After some research I decided to go the route of just mounting the directory that houses all my projects in the guest (I read this is what docker desktop does anyway `¯\_(ツ)_/¯`). This also means you can't run `podman compose` on the host, but what I do is just keep a terminal open with `vagrant ssh`. I also use [Powerlevel10k](https://github.com/romkatv/powerlevel10k) in the guest and host so I know where my commands are running just by looking at the command prompt. In any event, this means that I added a line to the Vagrantfile:
```
config.vm.synced_folder "/Users/jsicotte/Documents/workspaces", "/workspaces"
```

#### Networking
One of the things I really liked about Docker Mac was that if I opened a port I could just point my browser/tool to localhost:port and use the service. To get arond this issue I decided to use Traefik(https://traefik.io/) which is a docker aware reverse proxy. To make running Traefik fast ane easy, I created a docker compose file:
```
version: '3'

services:
  reverse-proxy:
    # The official v2 Traefik docker image
    image: traefik:v2.5
    # Enables the web UI and tells Traefik to listen to docker
    command: --api.insecure=true --providers.docker
    ports:
      # The HTTP port
      - "80:80"
      # The Web UI (enabled by --api.insecure=true)
      - "8080:8080"
    volumes:
      # So that Traefik can listen to the Docker events
      - /run/podman/podman.sock:/var/run/docker.sock
```
This works by starting the service and mounting the podman socket file (which emulates the docker socket file) in Traefik's container. This also means that I need to open two ports on the guest so I added these two lines to the Vagrantfile:
```
    config.vm.network "forwarded_port", guest: 80, host: 80
    config.vm.network "forwarded_port", guest: 8080, host: 8080
```
For a test, I fired up Minio with a compose file:
```
version: "3.7"
services:
    minio:
        hostname: minio
        image: docker.io/minio/minio
        ports:
            - 9003:9003
        environment:
            - MINIO_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
            - MINIO_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
        command: minio server /home/shared --console-address :9003
        labels:
            - traefik.http.routers.my-container.rule=Host(`minio.mysite.test`)
```
Unfortunately Traefik does not automatically detect and expose the service, so at minimum I had to add a label: `traefik.http.routers.my-container.rule`. The service is now detected, but I could not access it unless I specified the host with curl `curl -Hhost=minio.mysite.test localhost:80`.

#### More Networking: DNS
In order to make all this work with a browser on the host, I needed a way customize DNS so that the host header would be implicitly set correctly. Luckily there is a [Vagrant DNS plugin](https://github.com/BerlinVagrant/vagrant-dns). After installing the plugin I added more configuration to the Vagrantfile so that the DNS would properly resolve:

```
    config.dns.tld = "test"
    config.vm.hostname = "machine"
    config.vm.network :private_network, ip: "192.168.56.10"
    config.dns.patterns = [/^(\w+\.)*mysite\.test$/]
```
This now allows me to point my browser to: minio.mysite.test and see the Minio web console. However, when adding DNS it broke the Traefik user interface with cross domain errors. This was solved by adding the `traefik.frontend.headers.customResponseHeaders=Access-Control-Allow-Origin:*` label to the Traefik's docker compose file.

#### More Podman Features (I have not tested yet)
- The ability to take an existing docker compose configuration and produce k8 YAML.
- You can also run k8 YAML without the need a cluster setup such as minikube.
- [podman-macos](https://github.com/heyvito/podman-macos) provides a UI similar to Docker Desktop Mac. However this will not work with how I have it set up.

