def callback(self, pk=None, host_config_key='', extra_vars=None):
        """Contact Tower and request a configuration update using this job template.

        =====API DOCS=====
        Contact Tower and request a provisioning callback using this job template.

        :param pk: Primary key of the job template to run provisioning callback against.
        :type pk: int
        :param host_config_key: Key string used to authenticate the callback host.
        :type host_config_key: str
        :param extra_vars: Extra variables that are passed to provisioning callback.
        :type extra_vars: array of str
        :returns: A dictionary of a single key "changed", which indicates whether the provisioning callback
                  is successful.
        :rtype: dict

        =====API DOCS=====
        """
        url = self.endpoint + '%s/callback/' % pk
        if not host_config_key:
            host_config_key = client.get(url).json()['host_config_key']
        post_data = {'host_config_key': host_config_key}
        if extra_vars:
            post_data['extra_vars'] = parser.process_extra_vars(list(extra_vars), force_json=True)
        r = client.post(url, data=post_data, auth=None)
        if r.status_code == 201:
            return {'changed': True}