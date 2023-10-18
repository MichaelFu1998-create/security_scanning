def envelope(self):
        """ returns an :class:`Event` that can be used for site streams """

        def enveloped_event(data):
            return 'for_user' in data and self._func(data.get('message'))

        return self.__class__(enveloped_event, self.__name__)