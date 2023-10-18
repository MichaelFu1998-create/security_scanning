def tfpdef(self, ident_tok, annotation_opt):
        """(3.0-) tfpdef: NAME [':' test]"""
        if annotation_opt:
            colon_loc, annotation = annotation_opt
            return self._arg(ident_tok, colon_loc, annotation)
        return self._arg(ident_tok)