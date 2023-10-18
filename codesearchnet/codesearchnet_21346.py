def route(self, fn, **kwargs):
        """ Route helper : apply fn function but keep the calling object, *ie* kwargs, for other functions

        :param fn: Function to run the route with
        :type fn: function
        :param kwargs: Parsed url arguments
        :type kwargs: dict
        :return: HTTP Response with rendered template
        :rtype: flask.Response
        """
        new_kwargs = fn(**kwargs)

        # If there is no templates, we assume that the response is finalized :
        if not isinstance(new_kwargs, dict):
            return new_kwargs

        new_kwargs["url"] = kwargs
        return self.render(**new_kwargs)