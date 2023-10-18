def keyrelease(self, data):
        """
        Release key. NOTE: keypress should be called before this

        @param data: data to type.
        @type data: string

        @return: 1 on success.
        @rtype: integer
        """
        try:
            window = self._get_front_most_window()
        except (IndexError,):
            window = self._get_any_window()
        key_release_action = KeyReleaseAction(window, data)
        return 1