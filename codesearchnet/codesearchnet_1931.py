def subscriptlist(self, subscripts):
        """subscriptlist: subscript (',' subscript)* [',']"""
        if len(subscripts) == 1:
            return ast.Subscript(slice=subscripts[0], ctx=None, loc=None)
        elif all([isinstance(x, ast.Index) for x in subscripts]):
            elts  = [x.value for x in subscripts]
            loc   = subscripts[0].loc.join(subscripts[-1].loc)
            index = ast.Index(value=ast.Tuple(elts=elts, ctx=None,
                                              begin_loc=None, end_loc=None, loc=loc),
                              loc=loc)
            return ast.Subscript(slice=index, ctx=None, loc=None)
        else:
            extslice = ast.ExtSlice(dims=subscripts,
                                    loc=subscripts[0].loc.join(subscripts[-1].loc))
            return ast.Subscript(slice=extslice, ctx=None, loc=None)