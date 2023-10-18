def get_data(self, response):
        """ Get the data from the response """
        if self._response_list:
            return response
        elif self._response_key is None:
            if hasattr(response, "items"):
                for key, data in response.items():
                    if (hasattr(data, "__getitem__")
                            and not hasattr(data, "items")
                            and len(data) > 0
                            and 'id' in data[0]):
                        self._response_key = key
                        return data
            else:
                self._response_list = True
                return response
        else:
            return response[self._response_key]

        raise NoDataFound(response=response, url=self.request.get_url())