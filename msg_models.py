# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Aps(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=100)
    allowed_ap = models.IntegerField(blank=True, null=True)
    ap_deployment_mode = models.CharField(max_length=25, blank=True, null=True)
    ap_group = models.CharField(max_length=25, blank=True, null=True)
    cluster_id = models.CharField(max_length=100, blank=True, null=True)
    controller_name = models.CharField(max_length=100, blank=True, null=True)
    current_uplink_inuse = models.CharField(max_length=25, blank=True, null=True)
    down_reason = models.CharField(max_length=200, blank=True, null=True)
    ethernets = models.JSONField(blank=True, null=True)
    firmware_version = models.CharField(max_length=25, blank=True, null=True)
    gateway_cluster_id = models.CharField(max_length=200, blank=True, null=True)
    gateway_cluster_name = models.CharField(max_length=200, blank=True, null=True)
    group_name = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.CharField(max_length=25, blank=True, null=True)
    labels = models.JSONField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)
    macaddr = models.CharField(max_length=50, blank=True, null=True)
    mesh_role = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    modem_connected = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True, null=True)
    public_ip_address = models.CharField(max_length=25, blank=True, null=True)
    radios = models.JSONField(blank=True, null=True)
    serial = models.CharField(max_length=50)
    site_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    subnet_mask = models.CharField(max_length=25, blank=True, null=True)
    swarm_id = models.CharField(max_length=100, blank=True, null=True)
    swarm_master = models.IntegerField(blank=True, null=True)
    swarm_name = models.CharField(max_length=100, blank=True, null=True)
    last_refreshed = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aps'
        unique_together = (('customer_id', 'serial'),)


class Devices(models.Model):
    aruba_part_no = models.CharField(max_length=50, blank=True, null=True)
    customer_id = models.CharField(primary_key=True, max_length=100)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    device_type = models.CharField(max_length=50, blank=True, null=True)
    imei = models.CharField(max_length=50, blank=True, null=True)
    macaddr = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    serial = models.CharField(max_length=50)
    services = models.JSONField(blank=True, null=True)
    tier_type = models.CharField(max_length=45, blank=True, null=True)
    group_name = models.CharField(max_length=100, blank=True, null=True)
    configuration_error_status = models.IntegerField(blank=True, null=True)
    override_status = models.IntegerField(blank=True, null=True)
    template_name = models.CharField(max_length=100, blank=True, null=True)
    template_hash = models.CharField(max_length=50, blank=True, null=True)
    template_error_status = models.IntegerField(blank=True, null=True)
    site_name = models.CharField(max_length=100, blank=True, null=True)
    last_refreshed = models.DateTimeField(blank=True, null=True)
    error = models.IntegerField(blank=True, null=True)
    error_text = models.CharField(max_length=200, blank=True, null=True)
    auto_commit_state = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'devices'
        unique_together = (('customer_id', 'serial'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Groups(models.Model):
    group_name = models.CharField(primary_key=True, max_length=100)
    customer_id = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    aosversion = models.CharField(db_column='AOSVersion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    alloweddevtypes = models.JSONField(db_column='AllowedDevTypes', blank=True, null=True)  # Field name made lowercase.
    allowedswitchtypes = models.JSONField(db_column='AllowedSwitchTypes', blank=True, null=True)  # Field name made lowercase.
    apnetworkrole = models.CharField(db_column='APNetworkRole', max_length=25, blank=True, null=True)  # Field name made lowercase.
    architecture = models.CharField(max_length=25, blank=True, null=True)
    monitoronly = models.JSONField(db_column='MonitorOnly', blank=True, null=True)  # Field name made lowercase.
    gwnetworkrole = models.CharField(db_column='GwNetworkRole', max_length=50, blank=True, null=True)  # Field name made lowercase.
    monitoronlyswitch = models.IntegerField(db_column='MonitorOnlySwitch', blank=True, null=True)  # Field name made lowercase.
    last_refreshed = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'
        unique_together = (('group_name', 'customer_id'),)


class HomeCentralsites(models.Model):
    key = models.CharField(primary_key=True, max_length=200)
    username = models.CharField(max_length=200)
    site_id = models.CharField(max_length=25)
    address = models.CharField(max_length=200)
    associated_device_count = models.CharField(max_length=25)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)
    site_details = models.TextField()
    site_name = models.CharField(max_length=101)
    state = models.CharField(max_length=100)
    tags = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'home_centralsites'


class Ports(models.Model):
    serial = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50, blank=True, null=True)
    port_number = models.CharField(max_length=25)
    admin_state = models.CharField(max_length=25, blank=True, null=True)
    alignment = models.CharField(max_length=25, blank=True, null=True)
    allowed_vlan = models.JSONField(blank=True, null=True)
    duplex_mode = models.CharField(max_length=25, blank=True, null=True)
    has_poe = models.IntegerField(blank=True, null=True)
    in_errors = models.IntegerField(blank=True, null=True)
    out_errors = models.IntegerField(blank=True, null=True)
    intf_state_down_reason = models.CharField(max_length=50, blank=True, null=True)
    is_uplink = models.IntegerField(blank=True, null=True)
    macaddr = models.CharField(max_length=50, blank=True, null=True)
    mode = models.CharField(max_length=25, blank=True, null=True)
    mux = models.CharField(max_length=25, blank=True, null=True)
    oper_state = models.CharField(max_length=25, blank=True, null=True)
    phy_type = models.CharField(max_length=25, blank=True, null=True)
    poe_state = models.CharField(max_length=25, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    power_consumption = models.IntegerField(blank=True, null=True)
    rx_usage = models.IntegerField(blank=True, null=True)
    speed = models.CharField(max_length=25, blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    trusted = models.IntegerField(blank=True, null=True)
    tx_usage = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=25, blank=True, null=True)
    vlan = models.IntegerField(blank=True, null=True)
    vlan_mode = models.IntegerField(blank=True, null=True)
    vsx_enabled = models.IntegerField(blank=True, null=True)
    last_refreshed = models.DateTimeField(blank=True, null=True)
    customer_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ports'
        unique_together = (('serial', 'port_number'),)


class Sites(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=100)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    site_id = models.CharField(max_length=25)
    site_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    associated_device_count = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, null=True)
    last_refreshed = models.DateTimeField(blank=True, null=True)
    online = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sites'
        unique_together = (('customer_id', 'site_id'),)


class Switches(models.Model):
    firmware_version = models.CharField(max_length=25, blank=True, null=True)
    group_id = models.CharField(max_length=25, blank=True, null=True)
    group_name = models.CharField(max_length=45, blank=True, null=True)
    ip_address = models.CharField(max_length=25, blank=True, null=True)
    label_ids = models.JSONField(blank=True, null=True)
    labels = models.JSONField(blank=True, null=True)
    macaddr = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    public_ip_address = models.CharField(max_length=25, blank=True, null=True)
    serial = models.CharField(primary_key=True, max_length=50)
    site_name = models.CharField(max_length=100, blank=True, null=True)
    stack_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    switch_type = models.CharField(max_length=25, blank=True, null=True)
    uplink_ports = models.JSONField(blank=True, null=True)
    usage_int = models.IntegerField(blank=True, null=True)
    chassis_type = models.IntegerField(blank=True, null=True)
    commander_mac = models.CharField(max_length=25, blank=True, null=True)
    cpu_utilization = models.IntegerField(blank=True, null=True)
    default_gateway = models.CharField(max_length=25, blank=True, null=True)
    device_mode = models.IntegerField(blank=True, null=True)
    fan_speed = models.CharField(max_length=10, blank=True, null=True)
    max_power = models.IntegerField(blank=True, null=True)
    mem_free = models.IntegerField(blank=True, null=True)
    mem_total = models.IntegerField(blank=True, null=True)
    power_consumption = models.IntegerField(blank=True, null=True)
    poe_consumption = models.IntegerField(blank=True, null=True)
    temperature = models.IntegerField(blank=True, null=True)
    total_clients = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    uptime = models.IntegerField(blank=True, null=True)
    last_refreshed = models.DateTimeField(blank=True, null=True)
    customer_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'switches'


class Templates(models.Model):
    template_name = models.CharField(primary_key=True, max_length=100)
    customer_id = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    device_type = models.CharField(max_length=25, blank=True, null=True)
    group_name = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    template_hash = models.CharField(max_length=50, blank=True, null=True)
    version = models.CharField(max_length=25, blank=True, null=True)
    filename = models.CharField(max_length=100, blank=True, null=True)
    path = models.CharField(max_length=100, blank=True, null=True)
    last_refreshed = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'templates'
        unique_together = (('template_name', 'customer_id'),)


class Test1(models.Model):
    idtest1 = models.IntegerField(primary_key=True)
    test1col = models.CharField(max_length=45, blank=True, null=True)
    test1col1 = models.CharField(max_length=45, blank=True, null=True)
    test1col2 = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test1'


class Variables(models.Model):
    variable_name = models.CharField(primary_key=True, max_length=100)
    customer_id = models.CharField(max_length=100)
    value = models.CharField(max_length=6000, blank=True, null=True)
    serial = models.CharField(max_length=50)
    last_refreshed = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'variables'
        unique_together = (('variable_name', 'customer_id', 'serial'),)
