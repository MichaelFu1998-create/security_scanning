def make_index(self):
        """ Make the index mapping lines of actual code to their associated
        prefix comments.
        """
        for prev, block in zip(self.blocks[:-1], self.blocks[1:]):
            if not block.is_comment:
                self.index[block.start_lineno] = prev