def _from_xml(self, element):
        """Initialize an ErrorElement object from an XML element.

        :Parameters:
            - `element`: XML element to be decoded.
        :Types:
            - `element`: :etree:`ElementTree.Element`
        """
        # pylint: disable-msg=R0912
        if element.tag != self.error_qname:
            raise ValueError(u"{0!r} is not a {1!r} element".format(
                                                    element, self.error_qname))
        lang = element.get(XML_LANG_QNAME, None)
        if lang:
            self.language = lang
        self.condition = None
        for child in element:
            if child.tag.startswith(self.cond_qname_prefix):
                if self.condition is not None:
                    logger.warning("Multiple conditions in XMPP error element.")
                    continue
                self.condition = deepcopy(child)
            elif child.tag == self.text_qname:
                lang = child.get(XML_LANG_QNAME, None)
                if lang:
                    self.language = lang
                self.text = child.text.strip()
            else:
                bad = False
                for prefix in (STREAM_QNP, STANZA_CLIENT_QNP, STANZA_SERVER_QNP,
                                            STANZA_ERROR_QNP, STREAM_ERROR_QNP):
                    if child.tag.startswith(prefix):
                        logger.warning("Unexpected stream-namespaced"
                                                        " element in error.")
                        bad = True
                        break
                if not bad:
                    self.custom_condition.append( deepcopy(child) )
        if self.condition is None:
            self.condition = ElementTree.Element(self.cond_qname_prefix
                                                    + "undefined-condition")
        if self.condition.tag in OBSOLETE_CONDITIONS:
            new_cond_name = OBSOLETE_CONDITIONS[self.condition.tag]
            self.condition = ElementTree.Element(new_cond_name)