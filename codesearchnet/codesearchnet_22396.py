def post(self, url, params={}, files=None):
        """
        Issues a POST request against the API, allows for multipart data uploads

        :param url: a string, the url you are requesting
        :param params: a dict, the key-value of all the parameters needed
                       in the request
        :param files: a list, the list of tuples of files

        :returns: a dict parsed of the JSON response
        """
        params.update({'api_key': self.api_key})
        try:
            response = requests.post(self.host + url, data=params, files=files)
            return self.json_parse(response.content)
        except RequestException as e:
            return self.json_parse(e.args)