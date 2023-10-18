def delete_port(self, context, port_id, **kwargs):
        """Delete a port.

        :param context: neutron api request context.
        :param port_id: neutron port id.
        :param kwargs: optional kwargs.
        :raises IronicException: If the client is unable to delete the
            downstream port for any reason, the exception will be logged
            and IronicException raised.
        """
        LOG.info("delete_port %s %s" % (context.tenant_id, port_id))
        try:
            self._delete_port(context, port_id)
            LOG.info("deleted downstream port: %s" % (port_id))
        except Exception:
            LOG.error("failed deleting downstream port, it is now "
                      "orphaned! port_id: %s" % (port_id))