def on_key_press(self, symbol, modifiers):
        """
        Pyglet specific key press callback.
        Forwards and translates the events to :py:func:`keyboard_event`
        """
        self.keyboard_event(symbol, self.keys.ACTION_PRESS, modifiers)