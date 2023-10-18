def new_noncomment(self, start_lineno, end_lineno):
        """ We are transitioning from a noncomment to a comment.
        """
        block = NonComment(start_lineno, end_lineno)
        self.blocks.append(block)
        self.current_block = block