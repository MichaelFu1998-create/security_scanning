def single_input(self, body):
        """single_input: NEWLINE | simple_stmt | compound_stmt NEWLINE"""
        loc = None
        if body != []:
            loc = body[0].loc
        return ast.Interactive(body=body, loc=loc)