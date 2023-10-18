def keypress(self, data):
        """
        Press key. NOTE: keyrelease should be called

        @param data: data to type.
        @type data: string

        @return: 1 on success.
        @rtype: integer
        """
        try:
            window = self._get_front_most_window()
        except (IndexError,):
            window = self._get_any_window()
        key_press_action = KeyPressAction(window, data)
        return 1