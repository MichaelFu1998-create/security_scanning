def delete_sync(self, **kwargs):
        '''
        DELETE: delete data in the Firebase.
        Requires the 'point' parameter as a keyworded argument.
        '''
        self.amust(("point",), kwargs)
        response = requests.delete(self.url_correct(
            kwargs["point"],
            kwargs.get("auth", self.__auth)))
        self.catch_error(response)
        return response.content