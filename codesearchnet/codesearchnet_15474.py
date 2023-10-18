def t_less_variable(self, t):
        r'@@?[\w-]+|@\{[^@\}]+\}'
        v = t.value.lower()
        if v in reserved.tokens:
            t.type = reserved.tokens[v]
            if t.type == "css_media":
                t.lexer.push_state("mediaquery")
            elif t.type == "css_import":
                t.lexer.push_state("import")
        return t