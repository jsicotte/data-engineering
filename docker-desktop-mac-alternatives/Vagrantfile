$install = <<-SCRIPT
sudo apt update
sudo apt install -y zsh
sudo apt install -y git
sudo apt install -y podman
SCRIPT

Vagrant.configure("2") do |config|
    config.vm.box = "debian/bullseye64"
    config.vm.provision "shell", inline: $install
    config.vm.synced_folder "/Users/jsicotte/Documents/workspaces", "/workspaces"
    config.vm.network "forwarded_port", guest: 80, host: 80
    config.vm.network "forwarded_port", guest: 8080, host: 8080
    config.dns.tld = "test"
    config.vm.hostname = "machine"
    config.vm.network :private_network, ip: "192.168.56.10"
    config.dns.patterns = [/^(\w+\.)*mysite\.test$/]
end
