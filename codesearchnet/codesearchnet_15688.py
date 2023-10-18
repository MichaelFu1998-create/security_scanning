def generate_key(cls, secret_key, region, service, date,
                     intermediates=False):
        """
        Generate the signing key string as bytes.

        If intermediate is set to True, returns a 4-tuple containing the key
        and the intermediate keys:

        ( signing_key, date_key, region_key, service_key )

        The intermediate keys can be used for testing against examples from
        Amazon.

        """
        init_key = ('AWS4' + secret_key).encode('utf-8')
        date_key = cls.sign_sha256(init_key, date)
        region_key = cls.sign_sha256(date_key, region)
        service_key = cls.sign_sha256(region_key, service)
        key = cls.sign_sha256(service_key, 'aws4_request')
        if intermediates:
            return (key, date_key, region_key, service_key)
        else:
            return key