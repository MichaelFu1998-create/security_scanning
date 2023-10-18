def parse_string(self, string):
        """Parse a string into a Graph.

        :param string: String that is to be passed into Grapg
        :return: Graph
        """
        dom = minidom.parseString(string)
        return self.parse_dom(dom)