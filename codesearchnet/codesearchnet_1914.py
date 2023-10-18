def global_stmt(self, global_loc, names):
        """global_stmt: 'global' NAME (',' NAME)*"""
        return ast.Global(names=list(map(lambda x: x.value, names)),
                          name_locs=list(map(lambda x: x.loc, names)),
                          keyword_loc=global_loc, loc=global_loc.join(names[-1].loc))