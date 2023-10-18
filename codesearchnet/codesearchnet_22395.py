def get(self, url, params={}):
        """
        Issues a GET request against the API, properly formatting the params

        :param url: a string, the url you are requesting
        :param params: a dict, the key-value of all the paramaters needed
                       in the request
        :returns: a dict parsed of the JSON response
        """

        params.update({'api_key': self.api_key})
        try:
            response = requests.get(self.host + url, params=params)
        except RequestException as e:
            response = e.args

        return self.json_parse(response.content)