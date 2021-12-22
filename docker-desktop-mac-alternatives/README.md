# Docker Desktop Mac Alternatives
Since the licensing of Docker Desktop Mac has changed recently, there has been some interest in possible alternatives. Below is a possible list of alternatives.
The replacements are biased for my use cases: docker compse for basic prototype work and Kubernetes for prodution work.

## Investigation History
### Failed Attempt: lima-vm and nerdcl
At first I looked into using docker-machine since that is what I used prior to the Docker Desktop Mac, however maintenance stopped in 2019 and the project is now dead. Similarly, [boot2docker](https://github.com/boot2docker/boot2docker) is dead as well.

The next step was to look for a docker-machine alternative. This led me to [lima-vm](https://github.com/lima-vm/lima) which is a tool for setting Linux VMs on MacOS. Using this in conjuntion with a "drop in replacement for docker" [nerdctl](https://github.com/containerd/nerdctl), seemed like an option. However its version of compose `nerdctl compose up` is lacking too many features to be an easy replacement for `docker compose`.

### Mostly Functional: Podman
Moving on, I ran accross Podman. There used to be a `podman-machine` but it has since been deprecated and the docs essentially say "just use vagrant". [This article](https://marcusnoble.co.uk/2021-09-01-migrating-from-docker-to-podman/) on the topic of replacing Docker Mac with Podman is a great starting point.



## Option 1: Podman & Vagrant
There is not much to add on top of [this great article](https://marcusnoble.co.uk/2021-09-01-migrating-from-docker-to-podman/) on how to replace Docker Desktop with Podman. However some things I would like to highlight or add: 
- Podman has the ability to take an existing docker compose configuration and produce k8 YAML.
- You can also run k8 YAML without the need a cluster setup such as minikube.
- If you still need to run Docker Compose files I recommend taking a look at [podman-compose](https://github.com/containers/podman-compose).
- [podman-macos](https://github.com/containers/podman-compose) provides a UI similar to Docker Desktop Mac.

