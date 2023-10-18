def save_roster(self, dest, pretty = True):
        """Save the roster to an XML file.

        Can be used to save the last know roster copy for faster loading
        of a verisoned roster (if server supports that).

        :Parameters:
            - `dest`: file name or a file object
            - `pretty`: pretty-format the roster XML
        :Types:
            - `dest`: `str` or file-like object
            - `pretty`: `bool`
        """
        if self.roster is None:
            raise ValueError("No roster")
        element = self.roster.as_xml()
        if pretty:
            if len(element):
                element.text = u'\n  '
            p_child = None
            for child in element:
                if p_child is not None:
                    p_child.tail = u'\n  '
                if len(child):
                    child.text = u'\n    '
                p_grand = None
                for grand in child:
                    if p_grand is not None:
                        p_grand.tail = u'\n    '
                    p_grand = grand
                if p_grand is not None:
                    p_grand.tail = u'\n  '
                p_child = child
            if p_child is not None:
                p_child.tail = u"\n"
        tree = ElementTree.ElementTree(element)
        tree.write(dest, "utf-8")