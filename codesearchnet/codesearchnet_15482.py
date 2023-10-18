def token(self):
        """
        Token function. Contains 2 hacks:
            1.  Injects ';' into blocks where the last property
                leaves out the ;
            2.  Strips out whitespace from nonsignificant locations
                to ease parsing.
        """
        if self.next_:
            t = self.next_
            self.next_ = None
            return t
        while True:
            t = self.lexer.token()
            if not t:
                return t
            if t.type == 't_ws' and (
                    self.pretok or
                (self.last and self.last.type not in self.significant_ws)):
                continue
            self.pretok = False
            if t.type == 't_bclose' and self.last and self.last.type not in ['t_bopen', 't_bclose'] and self.last.type != 't_semicolon' \
                    and not (hasattr(t, 'lexer') and (t.lexer.lexstate == 'escapequotes' or t.lexer.lexstate == 'escapeapostrophe')):
                self.next_ = t
                tok = lex.LexToken()
                tok.type = 't_semicolon'
                tok.value = ';'
                tok.lineno = t.lineno
                tok.lexpos = t.lexpos
                self.last = tok
                self.lexer.in_property_decl = False
                return tok
            self.last = t
            break
        return t