def p_objectlist_2(self, p):
        "objectlist : objectlist COMMA objectitem"
        if DEBUG:
            self.print_p(p)
        p[0] = p[1] + [p[3]]