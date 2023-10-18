def post_sync(self, **kwargs):
        '''
        POST:  post data to a Firebase.
        Requires the 'point' parameter as a keyworded argument.
        Note: Firebase will give it a randomized "key"
        and the data will be the "value". Thus a key-value pair
        '''
        self.amust(("point", "data"), kwargs)
        response = requests.post(self.url_correct(
            kwargs["point"],
            kwargs.get("auth", self.__auth)),
            data=json.dumps(kwargs["data"]))
        self.catch_error(response)
        return response.content