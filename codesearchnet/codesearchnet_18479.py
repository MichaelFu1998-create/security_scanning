def valid(self, time: int = None) -> bool:
        """
        Is the token valid? This method only checks the timestamps within the
        token and compares them against the current time if none is provided.

        :param time: The timestamp to validate against
        :type time: Union[int, None]
        :return: The validity of the token.
        :rtype: bool
        """
        if time is None:
            epoch = datetime(1970, 1, 1, 0, 0, 0)
            now = datetime.utcnow()
            time = int((now - epoch).total_seconds())
        if isinstance(self.valid_from, int) and time < self.valid_from:
            return False
        if isinstance(self.valid_to, int) and time > self.valid_to:
            return False
        return True