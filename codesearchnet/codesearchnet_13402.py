def __make_fn(self):
        """Initialize the mandatory `self.fn` from `self.n`.

        This is a workaround for buggy clients which set only one of them."""
        s=[]
        if self.n.prefix:
            s.append(self.n.prefix)
        if self.n.given:
            s.append(self.n.given)
        if self.n.middle:
            s.append(self.n.middle)
        if self.n.family:
            s.append(self.n.family)
        if self.n.suffix:
            s.append(self.n.suffix)
        s=u" ".join(s)
        self.content["FN"]=VCardString("FN", s, empty_ok = True)