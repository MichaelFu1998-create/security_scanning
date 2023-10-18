def __parser(expression):
        """ adopted from Paul McGuire example. http://pyparsing.wikispaces.com/file/view/fourFn.py
        """
        expr_stack = []

        def push_first(strg, loc, toks):
            expr_stack.append(toks[0])

        def push_u_minus(strg, loc, toks):
            if toks and toks[0] == '-':
                expr_stack.append('unary -')

        point = Literal('.')
        _e = CaselessLiteral('E')
        fnumber = Combine(Word('+-' + nums, nums) +
                          Optional(point + Optional(Word(nums))) +
                          Optional(_e + Word('+-' + nums, nums)))
        ident = Word(alphas, alphas + nums + '_$')

        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        div = Literal("/")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        addop = plus | minus
        multop = mult | div
        expop = Literal("^")
        _pi = CaselessLiteral("PI")
        x = CaselessLiteral("X")

        expr = Forward()
        atom = (Optional("-") + (x | _pi | _e | fnumber | ident + lpar + expr + rpar).setParseAction(push_first) |
                (lpar + expr.suppress() + rpar)).setParseAction(push_u_minus)

        factor = Forward()
        factor << atom + ZeroOrMore((expop + factor).setParseAction(push_first))

        term = factor + ZeroOrMore((multop + factor).setParseAction(push_first))
        expr << term + ZeroOrMore((addop + term).setParseAction(push_first))

        expr.parseString(expression)
        return expr_stack