import sys
from mistral.actions.openstack.actions import NovaAction


class CheckFlavorAction(NovaAction):
    """Check if a hyoervisor has enough free resource to allocate
       an instance of the flavor type.
    """

    def __init__(self, migrate, hypervisor_hostname, flavor_id):
        self._flavor_id = flavor_id
        self._hypervisor_hostname = hypervisor_hostname
        self._migrate = migrate

    def run(self):
        client = self._get_client()

        if self._migrate:
            flavor_dict = client.flavors.find(id=str(self._flavor_id)).to_dict()
            hypervisors = client.hypervisors.list()
            for h in hypervisors:
                if (h.to_dict()["service"]["host"]==self._hypervisor_hostname):
                    hypervisor = h
                    break
            limits_dict = hypervisor.to_dict()

            mem = limits_dict['memory_mb'] - flavor_dict['ram']
            disk = limits_dict['free_disk_gb'] - flavor_dict['disk']
            vcpus = (limits_dict['vcpus']-limits_dict['vcpus_used']) - flavor_dict['vcpus']

            if ((mem<0) or (disk<0) or (vcpus<0)):
                sys.exit("hypervisor resource shortage for allocating this flavor!")
