def from_ssl_socket(cls, ssl_socket):
        """Get certificate data from an SSL socket.
        """
        try:
            data = ssl_socket.getpeercert(True)
        except AttributeError:
            # PyPy doesn't have .getpeercert
            data = None
        if not data:
            logger.debug("No certificate infromation")
            return cls()
        result = cls.from_der_data(data)
        result.validated = bool(ssl_socket.getpeercert())
        return result