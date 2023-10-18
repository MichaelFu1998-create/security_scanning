def get_sync(self, **kwargs):
        '''
        GET:  gets data from the Firebase.
        Requires the 'point' parameter as a keyworded argument.
        '''
        self.amust(("point",), kwargs)
        response = requests.get(self.url_correct(kwargs["point"],
                                kwargs.get("auth", self.__auth)))
        self.catch_error(response)
        return response.content