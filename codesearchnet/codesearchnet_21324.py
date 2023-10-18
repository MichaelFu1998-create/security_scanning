def transform(self, work, xml, objectId, subreference=None):
        """ Transform input according to potentially registered XSLT

        .. note:: Since 1.0.0, transform takes an objectId parameter which represent the passage which is called

        .. note:: Due to XSLT not being able to be used twice, we rexsltise the xml at every call of xslt

        .. warning:: Until a C libxslt error is fixed ( https://bugzilla.gnome.org/show_bug.cgi?id=620102 ), \
        it is not possible to use strip tags in the xslt given to this application

        :param work: Work object containing metadata about the xml
        :type work: MyCapytains.resources.inventory.Text
        :param xml: XML to transform
        :type xml: etree._Element
        :param objectId: Object Identifier
        :type objectId: str
        :param subreference: Subreference
        :type subreference: str
        :return: String representation of transformed resource
        :rtype: str
        """
        # We check first that we don't have
        if str(objectId) in self._transform:
            func = self._transform[str(objectId)]
        else:
            func = self._transform["default"]

        # If we have a string, it means we get a XSL filepath
        if isinstance(func, str):
            with open(func) as f:
                xslt = etree.XSLT(etree.parse(f))
            return etree.tostring(
                xslt(xml),
                encoding=str, method="html",
                xml_declaration=None, pretty_print=False, with_tail=True, standalone=None
            )

        # If we have a function, it means we return the result of the function
        elif isinstance(func, Callable):
            return func(work, xml, objectId, subreference)
        # If we have None, it means we just give back the xml
        elif func is None:
            return etree.tostring(xml, encoding=str)