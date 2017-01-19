# steps to configure and use the flows defined under mistral_recover_flows
1）（copy files）
$ cd /path/to/mistral/mistral/actions/openstack/
$ cp -r /path/to/senlin/examples/workflow/cluster_migration ./


2) (modify mistral/setup.cfg)
$ vim /path/to/mistral/setup.cfg:

[entry_points]
...
mistral.actions =
    ...
    custom.filter_vm = mistral.actions.openstack.cluster_migration.filter_vm_action:FilterVmAction
    custom.cold_migrate = mistral.actions.openstack.cluster_migration.cold_migration.cold_migrate_vm_action:ColdMigrateVmAction
    custom.live_migrate = mistral.actions.openstack.cluster_migration.live_migration.live_migrate_vm_action:LiveMigrateVmAction
    custom.validate_host = mistral.actions.openstack.cluster_migration.live_migration.validate_host_action:ValidateHostAction
    custom.wait_vm = mistral.actions.openstack.cluster_migration.cold_migration.wait_vm_action:WaitVmAction
    custom.confirm_resize = mistral.actions.openstack.cluster_migration.cold_migration.confirm_resize_vm_action:ConfirmResizeVmAction
    custom.validate_flavor = mistral.actions.openstack.cluster_migration.cold_migration.validate_flavor_action:ValidateFlavorAction


3) (populate db)
$ cd /path/to/mistral
$ sudo pip install -e .
$ mistral-db-manage —-config-file /path/to/mistral.conf populate


4) (create workflow)
$cd /path/to/mistral/mistral/actions/openstack/cluster_migration
$mistral workflow-create cold_migration/cluster-coldmigration.yaml
