def poll_once(self, timeout=0.0):
        """
        Poll active sockets once

        This method can be used to allow aborting server polling loop
        on some condition.

        :param timeout: polling timeout
        """
        if self._map:
            self._poll_func(timeout, self._map)