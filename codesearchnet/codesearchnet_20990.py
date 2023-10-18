def execute_undo(self, message):
        """
        Manage the response when the server rejects a message.

        An undo is when required this client sends a message that the server 
        refuses to pass on to the other clients playing the game.  When this 
        happens, the client must undo the changes that the message made to the 
        world before being sent or crash.  Note that unlike sync requests, undo 
        requests are only reported to the client that sent the offending 
        message.
        """
        info("undoing message: {message}")

        # Roll back changes that the original message made to the world.

        with self.world._unlock_temporarily():
            message._undo(self.world)
            self.world._react_to_undo_response(message)

        # Give the actors a chance to react to the error.  For example, a 
        # GUI actor might inform the user that there are connectivity 
        # issues and that their last action was countermanded.

        for actor in self.actors:
            actor._react_to_undo_response(message)