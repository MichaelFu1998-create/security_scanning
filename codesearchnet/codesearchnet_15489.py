def remove_block(self, block, index="-1"):
        """Remove block element from scope
        Args:
            block (Block): Block object
        """
        self[index]["__blocks__"].remove(block)
        self[index]["__names__"].remove(block.raw())