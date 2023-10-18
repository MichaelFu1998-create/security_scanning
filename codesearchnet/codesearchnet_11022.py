def on_mouse_motion(self, x, y, dx, dy):
        """
        Pyglet specific mouse motion callback.
        Forwards and traslates the event to :py:func:`cursor_event`
        """
        # screen coordinates relative to the lower-left corner
        self.cursor_event(x, self.buffer_height - y, dx, dy)