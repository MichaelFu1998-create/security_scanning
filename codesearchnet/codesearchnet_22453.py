def is_suspicious(self, result=None):
        """
        Check if IP is suspicious

        :param result: httpBL results; if None, then results from last check_ip() used (optional)
        :return: True or False
        """

        result = result if result is not None else self._last_result
        suspicious = False
        if result is not None:
            suspicious = True if result['type'] > 0 else False
        return suspicious