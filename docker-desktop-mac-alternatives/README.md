# Docker Desktop Mac Alternatives
Since the licensing of Docker Desktop Mac has changed recently, there has been some interest in possible alternatives. Below is a possible list of alternatives.
The replacements are biased for my use cases: docker compse for basic prototype work and Kubernetes for prodution work.

## Some Quick History
If you are like me and started out using docker-machine with VirtualBox and then happily migrated to using Docker Desktop Mac, there are a couple developments you might want to be aware of.
Though there has been some updates made to the docker-machine project, for all intents and purposes it has been dead since 2019. I would guess this is because of it being absorbed into `docker compose`. Similarly, [boot2docker](https://github.com/boot2docker/boot2docker) has been sunsetted in favor Docker Desktop.

## Option 1: Podman & Podman Compose
There is not much to add on top of [this great article](https://marcusnoble.co.uk/2021-09-01-migrating-from-docker-to-podman/) on how to replace Docker Desktop with Podman. However some things I would like to highlight or add: 
- Podman has the ability to take an existing docker compose configuration and produce k8 YAML.
- You can also run k8 YAML without the need a cluster setup such as minikube.
- If you still need to run Docker Compose files I recommend taking a look at [podman-compose](https://github.com/containers/podman-compose).
- [podman-macos](https://github.com/containers/podman-compose) provides a UI similar to Docker Desktop Mac.

## Option 2: lima-vm & nerdctl
The [lima-vm](https://github.com/lima-vm/lima) can essentially act like doker-machine and includes the [nerdctl](https://github.com/containerd/nerdctl) docker "drop in replacement". Though the project claims to be a replacement it still has a ways to go. For example it does not support specifying a service name with `nerdctl compose up`. It also lacks a UI and the k8 tooling that the podman toolset provides. These projects look promising, but I will stick with podman for my use.