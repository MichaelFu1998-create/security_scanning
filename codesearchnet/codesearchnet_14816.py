def create_port(self, context, network_id, port_id, **kwargs):
        """Create a port.

        :param context: neutron api request context.
        :param network_id: neutron network id.
        :param port_id: neutron port id.
        :param kwargs:
            required keys - device_id: neutron port device_id (instance_id)
                            instance_node_id: nova hypervisor host id
                            mac_address: neutron port mac address
                            base_net_driver: the base network driver
            optional keys - addresses: list of allocated IPAddress models
                            security_groups: list of associated security groups
        :raises IronicException: If the client is unable to create the
            downstream port for any reason, the exception will be logged
            and IronicException raised.
        """
        LOG.info("create_port %s %s %s" % (context.tenant_id, network_id,
                                           port_id))

        # sanity check
        if not kwargs.get('base_net_driver'):
            raise IronicException(msg='base_net_driver required.')
        base_net_driver = kwargs['base_net_driver']

        if not kwargs.get('device_id'):
            raise IronicException(msg='device_id required.')
        device_id = kwargs['device_id']

        if not kwargs.get('instance_node_id'):
            raise IronicException(msg='instance_node_id required.')
        instance_node_id = kwargs['instance_node_id']

        if not kwargs.get('mac_address'):
            raise IronicException(msg='mac_address is required.')
        mac_address = str(netaddr.EUI(kwargs["mac_address"]["address"]))
        mac_address = mac_address.replace('-', ':')

        # TODO(morgabra): Change this when we enable security groups.
        if kwargs.get('security_groups'):
            msg = 'ironic driver does not support security group operations.'
            raise IronicException(msg=msg)

        # unroll the given address models into a fixed_ips list we can
        # pass downstream
        fixed_ips = []
        addresses = kwargs.get('addresses')
        if not isinstance(addresses, list):
            addresses = [addresses]
        for address in addresses:
            fixed_ips.append(self._make_fixed_ip_dict(context, address))

        body = {
            "id": port_id,
            "network_id": network_id,
            "device_id": device_id,
            "device_owner": kwargs.get('device_owner', ''),
            "tenant_id": context.tenant_id or "quark",
            "roles": context.roles,
            "mac_address": mac_address,
            "fixed_ips": fixed_ips,
            "switch:hardware_id": instance_node_id,
            "dynamic_network": not STRATEGY.is_provider_network(network_id)
        }

        net_info = self._get_base_network_info(
            context, network_id, base_net_driver)
        body.update(net_info)

        try:
            LOG.info("creating downstream port: %s" % (body))
            port = self._create_port(context, body)
            LOG.info("created downstream port: %s" % (port))
            return {"uuid": port['port']['id'],
                    "vlan_id": port['port']['vlan_id']}
        except Exception as e:
            msg = "failed to create downstream port. Exception: %s" % (e)
            raise IronicException(msg=msg)