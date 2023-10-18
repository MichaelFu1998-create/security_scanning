def on_update_stage(self, dt):
        """
        Sequentially update the actors, the world, and the messaging system.  
        The theater terminates once all of the actors indicate that they are done.
        """

        for actor in self.actors:
            actor.on_update_game(dt)

        self.forum.on_update_game()

        with self.world._unlock_temporarily():
            self.world.on_update_game(dt)

        if self.world.has_game_ended():
            self.exit_stage()