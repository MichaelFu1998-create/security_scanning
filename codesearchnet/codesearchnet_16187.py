def _execute(self, command, data=None, unpack=True):
        """ Private method to execute command.

        Args:
            command(Command): The defined command.
            data(dict): The uri variable and body.
            uppack(bool): If unpack value from result.

        Returns:
            The unwrapped value field in the json response.
        """
        if not data:
            data = {}
        if self.session_id is not None:
            data.setdefault('session_id', self.session_id)
        data = self._wrap_el(data)
        res = self.remote_invoker.execute(command, data)
        ret = WebDriverResult.from_object(res)
        ret.raise_for_status()
        ret.value = self._unwrap_el(ret.value)
        if not unpack:
            return ret
        return ret.value