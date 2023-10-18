def make_list_elms_pretty(self):
        """ make any list element read like a list
        """
        for elm in self.parser.getElementsByTag(self.top_node, tag='li'):
            elm.text = r'• {}'.format(elm.text)