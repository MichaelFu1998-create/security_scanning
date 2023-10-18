def p_top(self, p):
        "top : objectlist"
        if DEBUG:
            self.print_p(p)
        p[0] = self.objectlist_flat(p[1], True)