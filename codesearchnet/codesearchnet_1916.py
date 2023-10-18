def nonlocal_stmt(self, nonlocal_loc, names):
        """(3.0-) nonlocal_stmt: 'nonlocal' NAME (',' NAME)*"""
        return ast.Nonlocal(names=list(map(lambda x: x.value, names)),
                            name_locs=list(map(lambda x: x.loc, names)),
                            keyword_loc=nonlocal_loc, loc=nonlocal_loc.join(names[-1].loc))