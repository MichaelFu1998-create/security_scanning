def statements(self):
        '''Return a list of statements

        This is done by joining together any rows that
        have continuations
        '''
        # FIXME: no need to do this every time; we should cache the
        # result
        if len(self.rows) == 0:
            return []

        current_statement = Statement(self.rows[0])
        current_statement.startline = self.rows[0].linenumber
        current_statement.endline = self.rows[0].linenumber
        statements = []
        for row in self.rows[1:]:
            if len(row) > 0 and row[0] == "...":
                # we found a continuation
                current_statement += row[1:]
                current_statement.endline = row.linenumber
            else:
                if len(current_statement) > 0:
                    # append current statement to the list of statements...
                    statements.append(current_statement)
                # start a new statement
                current_statement = Statement(row)
                current_statement.startline = row.linenumber
                current_statement.endline = row.linenumber

        if len(current_statement) > 0:
            statements.append(current_statement)

        # trim trailing blank statements
        while (len(statements[-1]) == 0 or 
               ((len(statements[-1]) == 1) and len(statements[-1][0]) == 0)):
            statements.pop()
        return statements