def comparison(self, lhs, rhs):
        """
        (2.6, 2.7) comparison: expr (comp_op expr)*
        (3.0, 3.1) comparison: star_expr (comp_op star_expr)*
        (3.2-) comparison: expr (comp_op expr)*
        """
        if len(rhs) > 0:
            return ast.Compare(left=lhs, ops=list(map(lambda x: x[0], rhs)),
                               comparators=list(map(lambda x: x[1], rhs)),
                               loc=lhs.loc.join(rhs[-1][1].loc))
        else:
            return lhs