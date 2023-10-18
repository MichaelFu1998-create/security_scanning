def diag_port(self, context, port_id, **kwargs):
        """Diagnose a port.

        :param context: neutron api request context.
        :param port_id: neutron port id.
        :param kwargs: optional kwargs.
        :raises IronicException: If the client is unable to fetch the
            downstream port for any reason, the exception will be
            logged and IronicException raised.
        """
        LOG.info("diag_port %s" % port_id)
        try:
            port = self._client.show_port(port_id)
        except Exception as e:
            msg = "failed fetching downstream port: %s" % (str(e))
            LOG.exception(msg)
            raise IronicException(msg=msg)
        return {"downstream_port": port}