def add_block(self, block):
        """Add block element to scope
        Args:
            block (Block): Block object
        """
        self[-1]['__blocks__'].append(block)
        self[-1]['__names__'].append(block.raw())