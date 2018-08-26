# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

nodes_config = (JSON.parse(File.read("local-vms.json")))['nodes']

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "bento/centos-7.5"

  nodes_config.each do |node|
    node_name   = node[0] # name of node
    node_values = node[1] # content of node

    config.vm.define node_name do |config|

      config.vm.hostname = node_name
      network_configs = node_values['network_configs']

      network_configs.each do |network_config|
        config.vm.network "private_network", 
            :ip => network_config[':ip'], 
            :name => network_config[':name'], 
            :adapter => network_config[':adapter']
      end

      # configures all forwarding ports in JSON array
      ports = node_values['ports']
      ports.each do |port|
        config.vm.network :forwarded_port,
          host:  port[':host'],
          guest: port[':guest'],
          id:    port[':id']
      end
    end
  end
end
