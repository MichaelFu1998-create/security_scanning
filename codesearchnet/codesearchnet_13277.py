def from_xml(cls, element):
        """Make a RosterItem from an XML element.

        :Parameters:
            - `element`: the XML element
        :Types:
            - `element`: :etree:`ElementTree.Element`

        :return: a freshly created roster item
        :returntype: `cls`
        """
        if element.tag != ITEM_TAG:
            raise ValueError("{0!r} is not a roster item".format(element))
        try:
            jid = JID(element.get("jid"))
        except ValueError:
            raise BadRequestProtocolError(u"Bad item JID")
        subscription = element.get("subscription")
        ask = element.get("ask")
        name = element.get("name")
        duplicate_group = False
        groups = set()
        for child in element:
            if child.tag != GROUP_TAG:
                continue
            group = child.text
            if group is None:
                group = u""
            if group in groups:
                duplicate_group = True
            else:
                groups.add(group)
        approved = element.get("approved")
        if approved == "true":
            approved = True
        elif approved in ("false", None):
            approved = False
        else:
            logger.debug("RosterItem.from_xml: got unknown 'approved':"
                            " {0!r}, changing to False".format(approved))
            approved = False
        result = cls(jid, name, groups, subscription, ask, approved)
        result._duplicate_group = duplicate_group
        return result