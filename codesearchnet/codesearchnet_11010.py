def key_event_callback(self, window, key, scancode, action, mods):
        """
        Key event callback for glfw.
        Translates and forwards keyboard event to :py:func:`keyboard_event`

        :param window: Window event origin
        :param key: The key that was pressed or released.
        :param scancode: The system-specific scancode of the key.
        :param action: GLFW_PRESS, GLFW_RELEASE or GLFW_REPEAT
        :param mods: Bit field describing which modifier keys were held down.
        """
        self.keyboard_event(key, action, mods)