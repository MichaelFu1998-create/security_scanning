def verify_roster_set(self, fix = False, settings = None):
        """Check if `self` is valid roster set item.

        For use on server to validate incoming roster sets.

        Valid item must have proper `subscription` value other and valid value
        for 'ask'. The lengths of name and group names must fit the configured
        limits.

        :Parameters:
            - `fix`: if `True` than replace invalid 'subscription' and 'ask'
              values with right defaults
            - `settings`: settings object providing the name limits
        :Types:
            - `fix`: `bool`
            - `settings`: `XMPPSettings`

        :Raise: `BadRequestProtocolError` if the item is invalid.
        """
        # pylint: disable=R0912
        try:
            self._verify((None, u"remove"), fix)
        except ValueError, err:
            raise BadRequestProtocolError(unicode(err))
        if self.ask:
            if fix:
                self.ask = None
            else:
                raise BadRequestProtocolError("'ask' in roster set")
        if self.approved:
            if fix:
                self.approved = False
            else:
                raise BadRequestProtocolError("'approved' in roster set")
        if settings is None:
            settings = XMPPSettings()
        name_length_limit = settings["roster_name_length_limit"]
        if self.name and len(self.name) > name_length_limit:
            raise NotAcceptableProtocolError(u"Roster item name too long")
        group_length_limit = settings["roster_group_name_length_limit"]
        for group in self.groups:
            if not group:
                raise NotAcceptableProtocolError(u"Roster group name empty")
            if len(group) > group_length_limit:
                raise NotAcceptableProtocolError(u"Roster group name too long")
        if self._duplicate_group:
            raise BadRequestProtocolError(u"Item group duplicated")