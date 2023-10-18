def on_enter_stage(self):
        """
        Prepare the actors, the world, and the messaging system to begin 
        playing the game.
        
        This method is guaranteed to be called exactly once upon entering the 
        game stage.
        """
        with self.world._unlock_temporarily():
            self.forum.connect_everyone(self.world, self.actors)

        # 1. Setup the forum.

        self.forum.on_start_game()

        # 2. Setup the world.

        with self.world._unlock_temporarily():
            self.world.on_start_game()

        # 3. Setup the actors.  Because this is done after the forum and the  
        #    world have been setup, this signals to the actors that they can 
        #    send messages and query the game world as usual.

        num_players = len(self.actors) - 1

        for actor in self.actors:
            actor.on_setup_gui(self.gui)

        for actor in self.actors:
            actor.on_start_game(num_players)