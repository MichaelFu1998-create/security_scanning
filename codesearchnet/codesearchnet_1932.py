def dictmaker(self, elts):
        """(2.6) dictmaker: test ':' test (',' test ':' test)* [',']"""
        return ast.Dict(keys=list(map(lambda x: x[0], elts)),
                        values=list(map(lambda x: x[2], elts)),
                        colon_locs=list(map(lambda x: x[1], elts)),
                        loc=None)