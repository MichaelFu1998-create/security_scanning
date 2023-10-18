def package_info(cls, package):
        """ All package info for given package """

        if package not in cls.package_info_cache:
            package_json_url = 'https://pypi.python.org/pypi/%s/json' % package

            try:
                logging.getLogger('requests').setLevel(logging.WARN)
                response = requests.get(package_json_url)
                response.raise_for_status()

                cls.package_info_cache[package] = simplejson.loads(response.text)

            except Exception as e:
                log.debug('Could not get package info from %s: %s', package_json_url, e)
                cls.package_info_cache[package] = None

        return cls.package_info_cache[package]