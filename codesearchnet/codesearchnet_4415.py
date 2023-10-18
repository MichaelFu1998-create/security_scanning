def send_UDP_message(self, message):
        """Send UDP message."""
        x = 0
        if self.tracking_enabled:
            try:
                proc = udp_messenger(self.domain_name, self.UDP_IP, self.UDP_PORT, self.sock_timeout, message)
                self.procs.append(proc)
            except Exception as e:
                logger.debug("Usage tracking failed: {}".format(e))
        else:
            x = -1

        return x