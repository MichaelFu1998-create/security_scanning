def execute_sync(self, message):
        """
        Respond when the server indicates that the client is out of sync.

        The server can request a sync when this client sends a message that 
        fails the check() on the server.  If the reason for the failure isn't 
        very serious, then the server can decide to send it as usual in the 
        interest of a smooth gameplay experience.  When this happens, the 
        server sends out an extra response providing the clients with the
        information they need to resync themselves.
        """
        info("synchronizing message: {message}")

        # Synchronize the world.

        with self.world._unlock_temporarily():
            message._sync(self.world)
            self.world._react_to_sync_response(message)

        # Synchronize the tokens.

        for actor in self.actors:
            actor._react_to_sync_response(message)