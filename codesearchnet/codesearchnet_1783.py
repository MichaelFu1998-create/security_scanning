def getfirstmatchingheader(self, name):
        """Get the first header line matching name.

        This is similar to getallmatchingheaders, but it returns only the
        first matching header (and its continuation lines).
        """
        name = name.lower() + ':'
        n = len(name)
        lst = []
        hit = 0
        for line in self.headers:
            if hit:
                if not line[:1].isspace():
                    break
            elif line[:n].lower() == name:
                hit = 1
            if hit:
                lst.append(line)
        return lst