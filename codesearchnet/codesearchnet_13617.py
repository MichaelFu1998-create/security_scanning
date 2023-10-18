def _connected(self):
        """Handle connection success."""
        self._auth_properties['remote-ip'] = self._dst_addr[0]
        if self._dst_service:
            self._auth_properties['service-domain'] = self._dst_name
        if self._dst_hostname is not None:
            self._auth_properties['service-hostname'] = self._dst_hostname
        else:
            self._auth_properties['service-hostname'] = self._dst_addr[0]
        self._auth_properties['security-layer'] = None
        self.event(ConnectedEvent(self._dst_addr))
        self._set_state("connected")
        self._stream.transport_connected()