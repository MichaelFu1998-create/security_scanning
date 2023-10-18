def _get_elements(self):
        '''
        Yields all elements as PathElements
        '''
        for index, el in enumerate(self._elements):
            if isinstance(el, tuple):
                el = PathElement(*el)
                self._elements[index] = el
            yield el