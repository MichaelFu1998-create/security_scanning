def process_token(self, kind, string, start, end, line):
        """ Process a single token.
        """
        if self.current_block.is_comment:
            if kind == tokenize.COMMENT:
                self.current_block.add(string, start, end, line)
            else:
                self.new_noncomment(start[0], end[0])
        else:
            if kind == tokenize.COMMENT:
                self.new_comment(string, start, end, line)
            else:
                self.current_block.add(string, start, end, line)