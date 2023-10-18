def _validate_many(args, specs, defaults,passed_conditions,value_conditions,
                  allow_unknowns,unknowns_spec): 
    '''
    Similar to validate but validates multiple objects at once, each with their own specification. 
    
    Fill objects that were specified but not provided with NotPassed or default values
    Apply `value_condition` to object dictionary as a whole 
    '''
    validated_args = builtins.dict() 
    passed_but_not_specified = set(args.keys()) - set(specs.keys())
    if passed_but_not_specified:
        if not allow_unknowns:
            raise ValueError(('Arguments {} were passed but not specified (use ' + 
                 '`allow_unknowns=True` to avoid this error)'.format(passed_but_not_specified)))
        else:
            for arg in passed_but_not_specified:
                if unknowns_spec is not None:
                    specs[arg] = unknowns_spec
    if passed_conditions:
        validate(args, Dict(passed_conditions=passed_conditions))
    for arg in specs:
        if (not arg in args) or NotPassed(args[arg]):
            if arg in defaults:
                if isinstance(defaults[arg],DefaultGenerator):
                    validated_args[arg] = defaults[arg]()
                else:
                    validated_args[arg] = defaults[arg]
            else:
                validated_args[arg] = NotPassed
        else:#Default values and NotPassed values are not validated. Former has advantage that default values need to be `correct` without validation and thus encourage the user to pass stuff that doesn't need validation, and is therefore faster
            validated_args[arg] = validate(args[arg], specs[arg])
    if value_conditions:
        validated_args = validate(validated_args, value_conditions)
    return validated_args