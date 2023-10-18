def get_data(self, *args, **kwargs):
        """
            Customized version of get_data to perform __check_actions_in_data
        """
        data = super(Droplet, self).get_data(*args, **kwargs)
        if "type" in kwargs:
            if kwargs["type"] == POST:
                self.__check_actions_in_data(data)
        return data