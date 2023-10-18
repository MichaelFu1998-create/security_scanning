def p_object_1(self, p):
        "object : LEFTBRACE objectlist COMMA RIGHTBRACE"
        if DEBUG:
            self.print_p(p)
        p[0] = self.objectlist_flat(p[2], False)