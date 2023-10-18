def _httplib2_init(username, password):
        """Used to instantiate a regular HTTP request object"""
        obj = httplib2.Http()
        if username and password:
            obj.add_credentials(username, password)
        return obj