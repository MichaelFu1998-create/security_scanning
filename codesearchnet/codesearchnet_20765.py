def pods(self):
        """Return list of all Pod objects in result"""
        # Return empty list if xml_tree is not defined (error Result object)
        if not self.xml_tree:
            return []

        # Create a Pod object for every pod group in xml
        return [Pod(elem) for elem in self.xml_tree.findall('pod')]