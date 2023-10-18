def formatter(self, api_client, data, newval):
        """Parse additional url fields and map them to inputs

        Attempt to create a dictionary with keys being user input, and
        response being the returned URL
        """
        if newval is None:
            return None

        user_param = data['_paramAdditionalUrls']
        urls = {}
        if isinstance(newval, str):
            urls[user_param[0]] = newval
        else:
            for key, url in zip(user_param, newval):
                urls[key] = url
        return urls