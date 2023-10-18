def on_key_release(self, symbol, modifiers):
        """
        Pyglet specific key release callback.
        Forwards and translates the events to :py:func:`keyboard_event`
        """
        self.keyboard_event(symbol, self.keys.ACTION_RELEASE, modifiers)