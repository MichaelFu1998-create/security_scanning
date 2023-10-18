def disconnect(self):
        """Gracefully disconnect from the server."""
        with self.lock:
            if self.stream:
                if self.settings[u"initial_presence"]:
                    self.send(Presence(stanza_type = "unavailable"))
                self.stream.disconnect()