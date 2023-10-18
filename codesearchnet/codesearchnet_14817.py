def update_port(self, context, port_id, **kwargs):
        """Update a port.

        :param context: neutron api request context.
        :param port_id: neutron port id.
        :param kwargs: optional kwargs.
        :raises IronicException: If the client is unable to update the
            downstream port for any reason, the exception will be logged
            and IronicException raised.

        TODO(morgabra) It does not really make sense in the context of Ironic
        to allow updating ports. fixed_ips and mac_address are burned in the
        configdrive on the host, and we otherwise cannot migrate a port between
        instances. Eventually we will need to support security groups, but for
        now it's a no-op on port data changes, and we need to rely on the
        API/Nova to not allow updating data on active ports.
        """
        LOG.info("update_port %s %s" % (context.tenant_id, port_id))

        # TODO(morgabra): Change this when we enable security groups.
        if kwargs.get("security_groups"):
            msg = 'ironic driver does not support security group operations.'
            raise IronicException(msg=msg)

        return {"uuid": port_id}