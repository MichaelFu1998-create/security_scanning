def getdelimited(self, beginchar, endchars, allowcomments = 1):
        """Parse a header fragment delimited by special characters.

        `beginchar' is the start character for the fragment.  If self is not
        looking at an instance of `beginchar' then getdelimited returns the
        empty string.

        `endchars' is a sequence of allowable end-delimiting characters.
        Parsing stops when one of these is encountered.

        If `allowcomments' is non-zero, embedded RFC 2822 comments are allowed
        within the parsed fragment.
        """
        if self.field[self.pos] != beginchar:
            return ''

        slist = ['']
        quote = 0
        self.pos += 1
        while self.pos < len(self.field):
            if quote == 1:
                slist.append(self.field[self.pos])
                quote = 0
            elif self.field[self.pos] in endchars:
                self.pos += 1
                break
            elif allowcomments and self.field[self.pos] == '(':
                slist.append(self.getcomment())
                continue        # have already advanced pos from getcomment
            elif self.field[self.pos] == '\\':
                quote = 1
            else:
                slist.append(self.field[self.pos])
            self.pos += 1

        return ''.join(slist)