def p_subidentifier(self, p):
        """subidentifier : fuzzy_lowercase_identifier
                         | NUMBER
                         | LOWERCASE_IDENTIFIER '(' NUMBER ')'"""
        n = len(p)
        if n == 2:
            p[0] = p[1]
        elif n == 5:
            # NOTE: we are not creating new symbol p[1] because formally
            # it is not defined in *this* MIB
            p[0] = (p[1], p[3])