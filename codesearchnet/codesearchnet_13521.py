def handle_tls_connected_event(self, event):
        """Verify the peer certificate on the `TLSConnectedEvent`.
        """
        if self.settings["tls_verify_peer"]:
            valid = self.settings["tls_verify_callback"](event.stream,
                                                        event.peer_certificate)
            if not valid:
                raise SSLError("Certificate verification failed")
        event.stream.tls_established = True
        with event.stream.lock:
            event.stream._restart_stream()