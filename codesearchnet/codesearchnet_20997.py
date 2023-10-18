def _remove_from_world(self):
        """
        Clear all the internal data the token needed while it was part of 
        the world.

        Note that this method doesn't actually remove the token from the 
        world.  That's what World._remove_token() does.  This method is just 
        responsible for setting the internal state of the token being removed.
        """
        self.on_remove_from_world()
        self._extensions = {}
        self._disable_forum_observation()
        self._world = None
        self._id = None