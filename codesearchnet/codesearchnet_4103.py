def append(self, row):
        ''' 
        The idea is, we recognize when we have a new testcase by 
        checking the first cell. If it's not empty and not a comment, 
        we have a new test case.

        '''
        if len(row) == 0:
            # blank line. Should we throw it away, or append a BlankLine object?
            return

        if (row[0] != "" and 
            (not row[0].lstrip().startswith("#"))):
            # we have a new child table
            self._children.append(self._childClass(self.parent, row.linenumber, row[0]))
            if len(row.cells) > 1:
                # It appears the first row -- which contains the test case or
                # keyword name -- also has the first logical row of cells.
                # We'll create a Row, but we'll make the first cell empty instead
                # of leaving the name in it, since other code always assumes the
                # first cell is empty. 
                #
                # To be honest, I'm not sure this is the Right Thing To Do, but 
                # I'm too lazy to audit the code to see if it matters if we keep 
                # the first cell intact. Sorry if this ends up causing you grief
                # some day...
                row[0] = ""
                self._children[-1].append(row.linenumber, row.raw_text, row.cells)

        elif len(self._children) == 0:
            # something before the first test case
            # For now, append it to self.comments; eventually we should flag
            # an error if it's NOT a comment
            self.comments.append(row)

        else:
            # another row for the testcase
            if len(row.cells) > 0:
                self._children[-1].append(row.linenumber, row.raw_text, row.cells)