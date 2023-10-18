def export_sync(self, **kwargs):
        '''
        EXPORT: exports data from the Firebase into a File, if given.
        Requires the 'point' parameter as a keyworded argument.
        '''
        self.amust(("point",), kwargs)
        response = requests.get(self.url_correct(kwargs["point"],
                                kwargs.get("auth", self.__auth), True))
        self.catch_error(response)
        path = kwargs.get("path", None)
        if path:
            self.__write(path, response.content, kwargs.get("mode", "w"))
        return response.content