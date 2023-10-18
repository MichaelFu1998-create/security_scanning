def limited(func):
    '''Decorator limiting resulting line length in order to avoid python parser stack overflow -
      If expression longer than LINE_LEN_LIMIT characters then it will be moved to upper line
     USE ONLY ON EXPRESSIONS!!! '''

    def f(standard=False, **args):
        insert_pos = len(
            inline_stack.names
        )  # in case line is longer than limit we will have to insert the lval at current position
        # this is because calling func will change inline_stack.
        # we cant use inline_stack.require here because we dont know whether line overflows yet
        res = func(**args)
        if len(res) > LINE_LEN_LIMIT:
            name = inline_stack.require('LONG')
            inline_stack.names.pop()
            inline_stack.names.insert(insert_pos, name)
            res = 'def %s(var=var):\n    return %s\n' % (name, res)
            inline_stack.define(name, res)
            return name + '()'
        else:
            return res

    f.__dict__['standard'] = func
    return f