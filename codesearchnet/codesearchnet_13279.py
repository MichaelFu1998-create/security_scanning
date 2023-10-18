def _verify(self, valid_subscriptions, fix):
        """Check if `self` is valid roster item.

        Valid item must have proper `subscription` and valid value for 'ask'.

        :Parameters:
            - `valid_subscriptions`: sequence of valid subscription values
            - `fix`: if `True` than replace invalid 'subscription' and 'ask'
              values with the defaults
        :Types:
            - `fix`: `bool`

        :Raise: `ValueError` if the item is invalid.
        """
        if self.subscription not in valid_subscriptions:
            if fix:
                logger.debug("RosterItem.from_xml: got unknown 'subscription':"
                        " {0!r}, changing to None".format(self.subscription))
                self.subscription = None
            else:
                raise ValueError("Bad 'subscription'")
        if self.ask not in (None, u"subscribe"):
            if fix:
                logger.debug("RosterItem.from_xml: got unknown 'ask':"
                                " {0!r}, changing to None".format(self.ask))
                self.ask = None
            else:
                raise ValueError("Bad 'ask'")