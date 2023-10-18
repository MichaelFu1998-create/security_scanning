def classdef__26(self, class_loc, name_tok, bases_opt, colon_loc, body):
        """(2.6, 2.7) classdef: 'class' NAME ['(' [testlist] ')'] ':' suite"""
        bases, lparen_loc, rparen_loc = [], None, None
        if bases_opt:
            lparen_loc, bases, rparen_loc = bases_opt

        return ast.ClassDef(name=name_tok.value, bases=bases, keywords=[],
                            starargs=None, kwargs=None, body=body,
                            decorator_list=[], at_locs=[],
                            keyword_loc=class_loc, lparen_loc=lparen_loc,
                            star_loc=None, dstar_loc=None, rparen_loc=rparen_loc,
                            name_loc=name_tok.loc, colon_loc=colon_loc,
                            loc=class_loc.join(body[-1].loc))