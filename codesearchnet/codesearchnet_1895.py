def file_input(parser, body):
        """file_input: (NEWLINE | stmt)* ENDMARKER"""
        body = reduce(list.__add__, body, [])
        loc = None
        if body != []:
            loc = body[0].loc
        return ast.Module(body=body, loc=loc)