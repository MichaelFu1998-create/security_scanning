def _heartbeat(self):
        """Start the heartbeat Greenlet to check connection health."""
        interval = self.config['heartbeat_interval']
        while self.connected:
            gevent.sleep(interval)
            # TODO: this process could use a timeout object like the disconnect
            #       timeout thing, and ONLY send packets when none are sent!
            #       We would do that by calling timeout.set() for a "sending"
            #       timeout.  If we're sending 100 messages a second, there is
            #       no need to push some heartbeats in there also.
            self.put_client_msg("2::")