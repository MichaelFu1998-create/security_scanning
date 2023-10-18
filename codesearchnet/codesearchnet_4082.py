def p_listitems_1(self, p):
        "listitems : listitems COMMA listitem"
        if DEBUG:
            self.print_p(p)
        p[0] = p[1] + [p[3]]