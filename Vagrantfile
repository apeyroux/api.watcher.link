# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "chef/ubuntu-14.04"
  config.vm.network "forwarded_port", guest: 5050, host: 5050
  config.vm.provision "shell", inline: "apt-get update; apt-get -y install python-pip python-dev mongodb phantomjs"
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
  end
end
