def prettify(self, elem):
        """Parse xml elements for pretty printing"""
        
        from xml.etree import ElementTree
        from re import sub
        
        rawString = ElementTree.tostring(elem, 'utf-8')
        parsedString = sub(r'(?=<[^/].*>)', '\n', rawString)  # Adds newline after each closing tag
        
        return parsedString[1:]