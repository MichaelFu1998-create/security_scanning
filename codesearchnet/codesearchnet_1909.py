def import_name(self, import_loc, names):
        """import_name: 'import' dotted_as_names"""
        return ast.Import(names=names,
                          keyword_loc=import_loc, loc=import_loc.join(names[-1].loc))