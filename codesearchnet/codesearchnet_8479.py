def is_equal_to(self, other, **kwargs):
        """Asserts that val is equal to other."""
        if self._check_dict_like(self.val, check_values=False, return_as_bool=True) and \
                self._check_dict_like(other, check_values=False, return_as_bool=True):
            if self._dict_not_equal(self.val, other, ignore=kwargs.get('ignore'), include=kwargs.get('include')):
                self._dict_err(self.val, other, ignore=kwargs.get('ignore'), include=kwargs.get('include'))
        else:
            if self.val != other:
                self._err('Expected <%s> to be equal to <%s>, but was not.' % (self.val, other))
        return self