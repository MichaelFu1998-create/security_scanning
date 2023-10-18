def nodes_to_check(self, docs):
        """\
        returns a list of nodes we want to search
        on like paragraphs and tables
        """
        nodes_to_check = []

        for doc in docs:
            for tag in ['p', 'pre', 'td']:
                items = self.parser.getElementsByTag(doc, tag=tag)
                nodes_to_check += items
        return nodes_to_check