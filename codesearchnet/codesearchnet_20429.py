def get_nginx_config(self):
        """
        Gets the Nginx config for the project

        """
        if os.path.exists(self._nginx_config):
            return open(self._nginx_config, 'r').read()
        else:
            return None