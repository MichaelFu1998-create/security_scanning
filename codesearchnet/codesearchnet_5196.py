def get_timeout(self):
        """
            Checks if any timeout for the requests to DigitalOcean is required.
            To set a timeout, use the REQUEST_TIMEOUT_ENV_VAR environment
            variable.
        """
        timeout_str = os.environ.get(REQUEST_TIMEOUT_ENV_VAR)
        if timeout_str:
            try:
                return float(timeout_str)
            except:
                self._log.error('Failed parsing the request read timeout of '
                                '"%s". Please use a valid float number!' %
                                        timeout_str)
        return None