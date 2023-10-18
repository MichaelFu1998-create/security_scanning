def detect_fold_level(self, prev_block, block):
        """
        Perfoms fold level detection for current block (take previous block
        into account).

        :param prev_block: previous block, None if `block` is the first block.
        :param block: block to analyse.
        :return: block fold level
        """
        # Python is an indent based language so use indentation for folding
        # makes sense but we restrict new regions to indentation after a ':',
        # that way only the real logical blocks are displayed.
        lvl = super(PythonFoldDetector, self).detect_fold_level(
            prev_block, block)
        # cancel false indentation, indentation can only happen if there is
        # ':' on the previous line
        prev_lvl = TextBlockHelper.get_fold_lvl(prev_block)
        if prev_block and lvl > prev_lvl and not (
                self._strip_comments(prev_block).endswith(':')):
            lvl = prev_lvl
        lvl = self._handle_docstrings(block, lvl, prev_block)
        lvl = self._handle_imports(block, lvl, prev_block)
        return lvl