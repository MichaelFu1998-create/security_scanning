def _releaseModifiers(self, modifiers, globally=False):
        """Release given modifiers (provided in list form).

        Parameters: modifiers list
        Returns: None
        """
        # Release them in reverse order from pressing them:
        modifiers.reverse()
        modFlags = self._pressModifiers(modifiers, pressed=False,
                                        globally=globally)
        return modFlags