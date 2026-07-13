============
Architecture
============

Hosts in the System
===================

In a system deployed by Kayobe we define a number of classes of hosts.

Ansible control host
    The Ansible control host is the host on which kayobe, kolla and
    kolla-ansible will be installed, and is typically where the cloud will be
    managed from.
Seed host
    The seed host runs the bifrost deploy container and is used to provision
    the overcloud hosts. By default, container images are built on the seed.
    Typically the seed host is deployed as a VM but this is not mandatory.
Seed hypervisor host
    The seed hypervisor host is configured with Libvirt and KVM. It hosts the
    seed VM (when the seed host is deployed as a VM) and infrastructure VMs.
Infrastructure VM hosts
    Infrastructure VMs (or Infra VMs) are virtual machines that may be deployed
    to provide supplementary infrastructure services. They may be for things
    like proxies or DNS servers that are dependencies of the overcloud hosts.
Overcloud hosts
    The overcloud hosts run the OpenStack control plane, network, monitoring,
    storage, and virtualised compute services. Typically the overcloud hosts
    run on bare metal, but this is not mandatory.
Bare metal workload hosts
    In a cloud providing bare metal workload services to tenants via ironic,
    these hosts will run the bare metal tenant workloads. In a cloud with only
    virtualised compute this category of hosts does not exist.

.. note::

   In many cases the Ansible control host and seed hypervisor will be the same,
   although this is not mandatory.

Overcloud Hosts
---------------

Overcloud hosts can further be divided into subclasses.

Controllers
    Controller hosts run the OpenStack control plane services.
Network
    Network hosts run the neutron networking services and load balancers for
    the OpenStack API services.
Monitoring
    Monitoring hosts run the control plane monitoring services.
Storage
    Storage hosts run the storage services.
Virtualised compute hypervisors
    Virtualised compute hypervisors run the tenant Virtual Machines (VMs) and
    associated OpenStack services for compute, networking and storage.

Networks
========

Kayobe's network configuration is very flexible but does define a few default
classes of networks. These are logical networks and may map to one or more
physical networks in the system.

Overcloud admin network
    The overcloud admin network is used to access the hosts in the system for
    administrative purposes, e.g. for remote SSH access.
Overcloud out-of-band network
    Name of the network used by the seed to access the out-of-band management
    controllers of the bare metal overcloud hosts.
Overcloud provisioning network
    The overcloud provisioning network is used by the seed host to provision
    the overcloud hosts.
Workload out-of-band network
    Name of the network used by the overcloud hosts to access the out-of-band
    management controllers of the bare metal workload hosts.
Workload provisioning network
    The workload provisioning network is used by the overcloud hosts to
    provision the bare metal workload hosts.
Cleaning network
    The cleaning network is used by the overcloud hosts to perform cleaning on
    the bare metal workload hosts.
Inspection network
    The inspection network is used by the overcloud hosts to perform hardware
    introspection on the bare metal workload hosts.
Internal network
    The internal network hosts the internal OpenStack API endpoints.
Public network
    The public network hosts the public OpenStack API endpoints.
External network
    The external network provides external network access for the hosts in the
    system.
Tunnel network
    The tunnel network carries tenant overlay network traffic.
Storage network
    The storage network carries storage data traffic.
Storage management network
    The storage management network carries storage management traffic.
