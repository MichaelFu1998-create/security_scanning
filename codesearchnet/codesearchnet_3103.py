def translate(self):
        """Translates outer operation and calls translate on inner operation.
           Returns fully translated code."""
        if not self.code:
            return ''
        new = bracket_replace(self.code)
        #Check comma operator:
        cand = new.split(',')  #every comma in new must be an operator
        if len(cand) > 1:  #LR
            return self.lr(cand, js_comma)
        #Check = operator:
        # dont split at != or !== or == or === or <= or >=
        #note <<=, >>= or this >>> will NOT be supported
        # maybe I will change my mind later
        # Find this crappy ?:
        if '?' in new:
            cond_ind = new.find('?')
            tenary_start = 0
            for ass in re.finditer(ASSIGNMENT_MATCH, new):
                cand = ass.span()[1]
                if cand < cond_ind:
                    tenary_start = cand
                else:
                    break
            actual_tenary = new[tenary_start:]
            spl = ''.join(split_at_any(new, [':', '?'], translate=trans))
            tenary_translation = transform_crap(spl)
            assignment = new[:tenary_start] + ' PyJsConstantTENARY'
            return trans(assignment).replace('PyJsConstantTENARY',
                                             tenary_translation)
        cand = list(split_at_single(new, '=', ['!', '=', '<', '>'], ['=']))
        if len(cand) > 1:  # RL
            it = reversed(cand)
            res = trans(it.next())
            for e in it:
                e = e.strip()
                if not e:
                    raise SyntaxError('Missing left-hand in assignment!')
                op = ''
                if e[-2:] in OP_METHODS:
                    op = ',' + e[-2:].__repr__()
                    e = e[:-2]
                elif e[-1:] in OP_METHODS:
                    op = ',' + e[-1].__repr__()
                    e = e[:-1]
                e = trans(e)
                #Now replace last get method with put and change args
                c = list(bracket_split(e, ['()']))
                beg, arglist = ''.join(c[:-1]).strip(), c[-1].strip(
                )  #strips just to make sure... I will remove it later
                if beg[-4:] != '.get':
                    raise SyntaxError('Invalid left-hand side in assignment')
                beg = beg[0:-3] + 'put'
                arglist = arglist[0:-1] + ', ' + res + op + ')'
                res = beg + arglist
            return res
        #Now check remaining 2 arg operators that are not handled by python
        #They all have Left to Right (LR) associativity
        order = [OR, AND, BOR, BXOR, BAND, EQS, COMPS, BSHIFTS, ADDS, MULTS]
        # actually we dont need OR and AND because they can be handled easier. But just for fun
        dangerous = ['<', '>']
        for typ in order:
            #we have to use special method for ADDS since they can be also unary operation +/++ or -/-- FUCK
            if '+' in typ:
                cand = list(split_add_ops(new))
            else:
                #dont translate. cant start or end on dangerous op.
                cand = list(
                    split_at_any(
                        new,
                        typ.keys(),
                        False,
                        dangerous,
                        dangerous,
                        validitate=comb_validitator))
            if not len(cand) > 1:
                continue
            n = 1
            res = trans(cand[0])
            if not res:
                raise SyntaxError("Missing operand!")
            while n < len(cand):
                e = cand[n]
                if not e:
                    raise SyntaxError("Missing operand!")
                if n % 2:
                    op = typ[e]
                else:
                    res = op(res, trans(e))
                n += 1
            return res
        #Now replace unary operators - only they are left
        cand = list(
            split_at_any(
                new, UNARY.keys(), False, validitate=unary_validitator))
        if len(cand) > 1:  #contains unary operators
            if '++' in cand or '--' in cand:  #it cant contain both ++ and --
                if '--' in cand:
                    op = '--'
                    meths = js_post_dec, js_pre_dec
                else:
                    op = '++'
                    meths = js_post_inc, js_pre_inc
                pos = cand.index(op)
                if cand[pos - 1].strip():  # post increment
                    a = cand[pos - 1]
                    meth = meths[0]
                elif cand[pos + 1].strip():  #pre increment
                    a = cand[pos + 1]
                    meth = meths[1]
                else:
                    raise SyntaxError('Invalid use of ++ operator')
                if cand[pos + 2:]:
                    raise SyntaxError('Too many operands')
                operand = meth(trans(a))
                cand = cand[:pos - 1]
            # now last cand should be operand and every other odd element should be empty
            else:
                operand = trans(cand[-1])
                del cand[-1]
            for i, e in enumerate(reversed(cand)):
                if i % 2:
                    if e.strip():
                        raise SyntaxError('Too many operands')
                else:
                    operand = UNARY[e](operand)
            return operand
        #Replace brackets
        if new[0] == '@' or new[0] == '#':
            if len(
                    list(bracket_split(new, ('#{', '@}')))
            ) == 1:  # we have only one bracket, otherwise pseudobracket like @@....
                assert new in REPL
                if new[0] == '#':
                    raise SyntaxError(
                        '[] cant be used as brackets! Use () instead.')
                return '(' + trans(REPL[new][1:-1]) + ')'
        #Replace function calls and prop getters
        # 'now' must be a reference like: a or b.c.d but it can have also calls or getters ( for example a["b"](3))
        #From here @@ means a function call and ## means get operation (note they dont have to present)
        it = bracket_split(new, ('#{', '@}'))
        res = []
        for e in it:
            if e[0] != '#' and e[0] != '@':
                res += [x.strip() for x in e.split('.')]
            else:
                res += [e.strip()]
        # res[0] can be inside @@ (name)...
        res = filter(lambda x: x, res)
        if is_internal(res[0]):
            out = res[0]
        elif res[0][0] in {'#', '@'}:
            out = '(' + trans(REPL[res[0]][1:-1]) + ')'
        elif is_valid_lval(
                res[0]) or res[0] in {'this', 'false', 'true', 'null'}:
            out = 'var.get(' + res[0].__repr__() + ')'
        else:
            if is_reserved(res[0]):
                raise SyntaxError('Unexpected reserved word: "%s"' % res[0])
            raise SyntaxError('Invalid identifier: "%s"' % res[0])
        if len(res) == 1:
            return out
        n = 1
        while n < len(res):  #now every func call is a prop call
            e = res[n]
            if e[0] == '@':  # direct call
                out += trans_args(REPL[e])
                n += 1
                continue
            args = False  #assume not prop call
            if n + 1 < len(res) and res[n + 1][0] == '@':  #prop call
                args = trans_args(REPL[res[n + 1]])[1:]
                if args != ')':
                    args = ',' + args
            if e[0] == '#':
                prop = trans(REPL[e][1:-1])
            else:
                if not is_lval(e):
                    raise SyntaxError('Invalid identifier: "%s"' % e)
                prop = e.__repr__()
            if args:  # prop call
                n += 1
                out += '.callprop(' + prop + args
            else:  #prop get
                out += '.get(' + prop + ')'
            n += 1
        return out