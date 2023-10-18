def put_sync(self, **kwargs):
        '''
        PUT:  puts data into the Firebase.
        Requires the 'point' parameter as a keyworded argument.
        '''
        self.amust(("point", "data"), kwargs)
        response = requests.put(self.url_correct(kwargs["point"],
                                kwargs.get("auth", self.__auth)),
                                data=json.dumps(kwargs["data"]))
        self.catch_error(response)
        return response.content