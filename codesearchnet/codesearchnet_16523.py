def __tokenize(self,string):
        """Split s into tokens and update the token buffer.

        __tokenize(string)

        New tokens are appended to the token buffer, discarding white
        space.  Based on http://effbot.org/zone/xml-scanner.htm
        """
        for m in self.dx_regex.finditer(string.strip()):
            code = m.lastgroup
            text = m.group(m.lastgroup)
            tok = Token(code,text)
            if not tok.iscode('WHITESPACE'):
                 self.tokens.append(tok)