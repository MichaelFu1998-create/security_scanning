def _get_base_url(base_url, api, version):
        """
            create the base url for the api

        Parameters
        ----------
        base_url : str
            format of the base_url using {api} and {version}
        api : str
            name of the api to use
        version : str
            version of the api

        Returns
        -------
        str
            the base url of the api you want to use
        """
        format_args = {}

        if "{api}" in base_url:
            if api == "":
                base_url = base_url.replace('{api}.', '')
            else:
                format_args['api'] = api

        if "{version}" in base_url:
            if version == "":
                base_url = base_url.replace('/{version}', '')
            else:
                format_args['version'] = version

        return base_url.format(api=api, version=version)