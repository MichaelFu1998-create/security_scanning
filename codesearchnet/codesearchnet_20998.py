def _unlock_temporarily(self):
        """
        Allow tokens to modify the world for the duration of a with-block.

        It's important that tokens only modify the world at appropriate times, 
        otherwise the changes they make may not be communicated across the 
        network to other clients.  To help catch and prevent these kinds of 
        errors, the game engine keeps the world locked most of the time and 
        only briefly unlocks it (using this method) when tokens are allowed to 
        make changes.  When the world is locked, token methods that aren't 
        marked as being read-only can't be called.  When the world is unlocked, 
        any token method can be called.  These checks can be disabled by 
        running python with optimization enabled.

        You should never call this method manually from within your own game.  
        This method is intended to be used by the game engine, which was 
        carefully designed to allow the world to be modified only when safe.  
        Calling this method yourself disables an important safety check.
        """
        if not self._is_locked:
            yield
        else:
            try:
                self._is_locked = False
                yield
            finally:
                self._is_locked = True