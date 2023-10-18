def new_comment(self, string, start, end, line):
        """ Possibly add a new comment.

        Only adds a new comment if this comment is the only thing on the line.
        Otherwise, it extends the noncomment block.
        """
        prefix = line[:start[1]]
        if prefix.strip():
            # Oops! Trailing comment, not a comment block.
            self.current_block.add(string, start, end, line)
        else:
            # A comment block.
            block = Comment(start[0], end[0], string)
            self.blocks.append(block)
            self.current_block = block