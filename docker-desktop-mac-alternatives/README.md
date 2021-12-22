# Docker Desktop Mac Alternatives
Since the licensing of Docker Desktop Mac has changed recently, there has been some interest in possible alternatives. Below is a possible list of alternatives.
The replacements are biased for my use cases: docker compse for basic prototype work and Kubernetes for prodution work.

## Investigation History
### Failed Attempt: lima-vm and nerdcl
At first I looked into using docker-machine since that is what I used prior to the Docker Desktop Mac, however maintenance stopped in 2019 and the project is now dead. Similarly, [boot2docker](https://github.com/boot2docker/boot2docker) is dead as well.

The next step was to look for a docker-machine alternative. This led me to [lima-vm](https://github.com/lima-vm/lima) which is a tool for setting Linux VMs on MacOS. Using this in conjuntion with a "drop in replacement for docker" [nerdctl](https://github.com/containerd/nerdctl), seemed like an option. However its version of compose `nerdctl compose up` is lacking too many features to be an easy replacement for `docker compose`.

### Mostly Functional: Podman
Moving on, I ran accross Podman. There used to be a `podman-machine` but it has since been deprecated and the docs essentially say "just use vagrant". [This article](https://marcusnoble.co.uk/2021-09-01-migrating-from-docker-to-podman/) on the topic of replacing Docker Mac with Podman is a great starting point.

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
I could run `podman compose up` from the MacOS host, but podman only has access to the filesystem of the Linux guest. After some research I decided to go the route of just mounting the directory that houses all my projects in the guest (I read this is what docker desktop does anyway `¯\_(ツ)_/¯`). This also means you can't run `podman compose` on the host, but what I do is just keep a terminal open with `vagrant ssh`. I also use [Powerlevel10k](https://github.com/romkatv/powerlevel10k) in the guest and host so I know where my commands are running just by looking at the command prompt.


## Option 1: Podman & Vagrant
- Podman has the ability to take an existing docker compose configuration and produce k8 YAML.
- You can also run k8 YAML without the need a cluster setup such as minikube.
- [podman-macos](https://github.com/containers/podman-compose) provides a UI similar to Docker Desktop Mac.

