def _parse(self, e, tag):
        
        """ Parses the text data from an XML element defined by tag.
        """
        
        tags = e.getElementsByTagName(tag)
        children = tags[0].childNodes
        if len(children) != 1: return None
        assert children[0].nodeType == xml.dom.minidom.Element.TEXT_NODE
        
        s = children[0].nodeValue
        s = format_data(s)
        s = replace_entities(s)
        
        return s