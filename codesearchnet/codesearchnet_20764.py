def query(self, input = '', params = {}):
        """Query Wolfram Alpha and return a Result object"""
        # Get and construct query parameters
        # Default parameters
        payload = {'input': input,
                    'appid': self.appid}
        # Additional parameters (from params), formatted for url
        for key, value in params.items():
            # Check if value is list or tuple type (needs to be comma joined)
            if isinstance(value, (list, tuple)):
                payload[key] = ','.join(value)
            else:
                payload[key] = value

        # Catch any issues with connecting to Wolfram Alpha API
        try:
            r = requests.get("http://api.wolframalpha.com/v2/query", params=payload)

            # Raise Exception (to be returned as error)
            if r.status_code != 200:
                raise Exception('Invalid response status code: %s' % (r.status_code))
            if r.encoding != 'utf-8':
                raise Exception('Invalid encoding: %s' % (r.encoding))

        except Exception, e:
            return Result(error = e)

        return Result(xml = r.text)