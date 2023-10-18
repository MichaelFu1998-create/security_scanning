def receive_id_from_server(self):
        """
        Listen for an id from the server.

        At the beginning of a game, each client receives an IdFactory from the 
        server.  This factory are used to give id numbers that are guaranteed 
        to be unique to tokens that created locally.  This method checks to see if such 
        a factory has been received.  If it hasn't, this method does not block 
        and immediately returns False.  If it has, this method returns True 
        after saving the factory internally.  At this point it is safe to enter 
        the GameStage.
        """
        for message in self.pipe.receive():
            if isinstance(message, IdFactory):
                self.actor_id_factory = message
                return True
        return False