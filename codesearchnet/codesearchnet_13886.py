def _parse(self, str):
        
        """ Parses the text data from an XML element defined by tag.
        """
        
        str = replace_entities(str)
        str = strip_tags(str)
        str = collapse_spaces(str)
        return str