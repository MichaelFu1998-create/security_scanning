def _get_find_dict(self, c, **kwargs):
        '''
        Return a dict that can be used in the return list of the :meth:`find`
        method.

        :param c: A :class:`skosprovider.skos.Concept` or
            :class:`skosprovider.skos.Collection`.
        :rtype: dict
        '''
        language = self._get_language(**kwargs)
        return {
            'id': c.id,
            'uri': c.uri,
            'type': c.type,
            'label': None if c.label() is None else c.label(language).label
        }