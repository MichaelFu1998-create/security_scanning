def generate_local_url(self, js_name):
        """
        Generate the local url for a js file.
        :param js_name:
        :return:
        """
        host = self._settings['local_host'].format(**self._host_context).rstrip('/')
        return '{}/{}.js'.format(host, js_name)