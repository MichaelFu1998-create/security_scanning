def process_file(self, file):
        """ Process a file object.
        """
        if sys.version_info[0] >= 3:
            nxt = file.__next__
        else:
            nxt = file.next
        for token in tokenize.generate_tokens(nxt):
            self.process_token(*token)
        self.make_index()