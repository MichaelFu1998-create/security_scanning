def on_exit_stage(self):
        """
        Give the actors, the world, and the messaging system a chance to react 
        to the end of the game.
        """

        # 1. Let the forum react to the end of the game.  Local forums don't 
        #    react to this, but remote forums take the opportunity to stop 
        #    trying to extract tokens from messages.

        self.forum.on_finish_game()

        # 2. Let the actors react to the end of the game.

        for actor in self.actors:
            actor.on_finish_game()

        # 3. Let the world react to the end of the game.

        with self.world._unlock_temporarily():
            self.world.on_finish_game()