def verify_roster_push(self, fix = False):
        """Check if `self` is valid roster push item.

        Valid item must have proper `subscription` value other and valid value
        for 'ask'.

        :Parameters:
            - `fix`: if `True` than replace invalid 'subscription' and 'ask'
              values with the defaults
        :Types:
            - `fix`: `bool`

        :Raise: `ValueError` if the item is invalid.
        """
        self._verify((None, u"from", u"to", u"both", u"remove"), fix)