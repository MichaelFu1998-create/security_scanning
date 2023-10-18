def build(self, pre=None, shortest=False):
        """Build the ``Quote`` instance

        :param list pre: The prerequisites list
        :param bool shortest: Whether or not the shortest reference-chain (most minimal) version of the field should be generated.
        """
        res = super(Q, self).build(pre, shortest=shortest)

        if self.escape:
            return repr(res)
        elif self.html_js_escape:
            return ("'" + res.encode("string_escape").replace("<", "\\x3c").replace(">", "\\x3e") + "'")
        else:
            return "".join([self.quote, res, self.quote])