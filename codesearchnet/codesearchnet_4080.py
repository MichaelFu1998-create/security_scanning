def p_block_0(self, p):
        "block : blockId object"
        if DEBUG:
            self.print_p(p)
        p[0] = (p[1], p[2])