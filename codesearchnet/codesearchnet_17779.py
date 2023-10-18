def validate(arg, spec):
    '''
    Make sure `arg` adheres to specification
    
    :param arg: Anything
    :param spec: Specification
    :type spec: Specification
    
    :return: Validated object
    '''
    rejection_subreason = None
    if spec is None:
        return arg
    try:
        return spec._validate(arg)
    except Exception as e:
        rejection_subreason = e
    try:
        lenience = spec.lenience
    except AttributeError:
        pass
    else:
        for level in range(1, lenience + 1):
            temp = None
            try:
                temp = spec.forgive(arg=arg, level=level)
            except Exception:
                pass  # Forgiving might fail, it is very hard to predict what happens when you do stuff to things that aren't what you think
            if temp is not None and temp is not arg:
                arg = temp
                try:
                    return spec._validate(arg)
                except Exception as e:
                    rejection_subreason = e
    rejection_reason = '`{}` was rejected by `{}`.'.format(arg, spec)
    rejection_subreason = ' ({}: {})'.format(rejection_subreason.__class__.__name__, rejection_subreason) if rejection_subreason is not None else ''
    raise ValidationError(rejection_reason + rejection_subreason)