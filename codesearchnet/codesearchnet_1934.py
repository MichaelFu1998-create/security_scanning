def classdef__30(self, class_loc, name_tok, arglist_opt, colon_loc, body):
        """(3.0) classdef: 'class' NAME ['(' [testlist] ')'] ':' suite"""
        arglist, lparen_loc, rparen_loc = [], None, None
        bases, keywords, starargs, kwargs = [], [], None, None
        star_loc, dstar_loc = None, None
        if arglist_opt:
            lparen_loc, arglist, rparen_loc = arglist_opt
            bases, keywords, starargs, kwargs = \
                arglist.args, arglist.keywords, arglist.starargs, arglist.kwargs
            star_loc, dstar_loc = arglist.star_loc, arglist.dstar_loc

        return ast.ClassDef(name=name_tok.value, bases=bases, keywords=keywords,
                            starargs=starargs, kwargs=kwargs, body=body,
                            decorator_list=[], at_locs=[],
                            keyword_loc=class_loc, lparen_loc=lparen_loc,
                            star_loc=star_loc, dstar_loc=dstar_loc, rparen_loc=rparen_loc,
                            name_loc=name_tok.loc, colon_loc=colon_loc,
                            loc=class_loc.join(body[-1].loc))