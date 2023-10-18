def attach(self, observer):
        """ Attach an observer.

        Args:
            observer (func): A function to be called when new messages arrive

        Returns:
            :class:`Stream`. Current instance to allow chaining
        """
        if not observer in self._observers:
            self._observers.append(observer)
        return self