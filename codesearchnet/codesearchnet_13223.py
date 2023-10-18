def update(self, **kwargs):
        '''Update the attributes of a JObject.

        Parameters
        ----------
        kwargs
            Keyword arguments of the form `attribute=new_value`

        Examples
        --------
        >>> J = jams.JObject(foo=5)
        >>> J.dumps()
        '{"foo": 5}'
        >>> J.update(bar='baz')
        >>> J.dumps()
        '{"foo": 5, "bar": "baz"}'
        '''
        for name, value in six.iteritems(kwargs):
            setattr(self, name, value)