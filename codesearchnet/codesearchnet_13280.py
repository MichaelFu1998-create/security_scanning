def verify_roster_result(self, fix = False):
        """Check if `self` is valid roster item.

        Valid item must have proper `subscription` value other than 'remove'
        and valid value for 'ask'.

        :Parameters:
            - `fix`: if `True` than replace invalid 'subscription' and 'ask'
              values with the defaults
        :Types:
            - `fix`: `bool`

        :Raise: `ValueError` if the item is invalid.
        """
        self._verify((None, u"from", u"to", u"both"), fix)