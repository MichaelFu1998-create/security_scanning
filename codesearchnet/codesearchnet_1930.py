def power(self, atom, trailers, factor_opt):
        """power: atom trailer* ['**' factor]"""
        for trailer in trailers:
            if isinstance(trailer, ast.Attribute) or isinstance(trailer, ast.Subscript):
                trailer.value = atom
            elif isinstance(trailer, ast.Call):
                trailer.func = atom
            trailer.loc = atom.loc.join(trailer.loc)
            atom = trailer
        if factor_opt:
            op_loc, factor = factor_opt
            return ast.BinOp(left=atom, op=ast.Pow(loc=op_loc), right=factor,
                             loc=atom.loc.join(factor.loc))
        return atom