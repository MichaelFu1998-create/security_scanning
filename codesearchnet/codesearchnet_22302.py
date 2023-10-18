def update_sync(self, **kwargs):
        '''
        UPDATE: updates data in the Firebase.
        Requires the 'point' parameter as a keyworded argument.
        '''
        self.amust(("point", "data"), kwargs)
        # Sending the 'PATCH' request
        response = requests.patch(self.url_correct(
            kwargs["point"],
            kwargs.get("auth", self.__auth)),
            data=json.dumps(kwargs["data"]))
        self.catch_error(response)
        return response.content