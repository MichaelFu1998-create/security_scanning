def cursor_event(self, x, y, dx, dy):
        """
        The standard mouse movement event method.
        Can be overriden to add new functionality.
        By default this feeds the system camera with new values.

        Args:
            x: The current mouse x position
            y: The current mouse y position
            dx: Delta x postion (x position difference from the previous event)
            dy: Delta y postion (y position difference from the previous event)
        """
        self.sys_camera.rot_state(x, y)