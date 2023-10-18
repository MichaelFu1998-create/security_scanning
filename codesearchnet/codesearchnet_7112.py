def nested_formula_parser(formula, check=True):
    r'''Improved formula parser which handles braces and their multipliers, 
    as well as rational element counts.

    Strips charges from the end of a formula first. Accepts repeated chemical
    units. Performs no sanity checking that elements are actually elements.
    As it uses regular expressions for matching, errors are mostly just ignored.
    
    Parameters
    ----------
    formula : str
        Formula string, very simply formats only.
    check : bool
        If `check` is True, a simple check will be performed to determine if
        a formula is not a formula and an exception will be raised if it is
        not, [-]

    Returns
    -------
    atoms : dict
        dictionary of counts of individual atoms, indexed by symbol with
        proper capitalization, [-]

    Notes
    -----
    Inspired by the approach taken by CrazyMerlyn on a reddit DailyProgrammer
    challenge, at https://www.reddit.com/r/dailyprogrammer/comments/6eerfk/20170531_challenge_317_intermediate_counting/

    Examples
    --------
    >>> pprint(nested_formula_parser('Pd(NH3)4.0001+2'))
    {'H': 12.0003, 'N': 4.0001, 'Pd': 1}
    '''
    formula = formula.replace('[', '').replace(']', '')
    charge_splits = bracketed_charge_re.split(formula)
    if len(charge_splits) > 1:
        formula = charge_splits[0]
    else:
        formula = formula.split('+')[0].split('-')[0]
    
    stack = [[]]
    last = stack[0]
    tokens = formula_token_matcher_rational.findall(formula)
    # The set of letters in the tokens should match the set of letters
    if check:
        token_letters = set([j for i in tokens for j in i if j in letter_set])
        formula_letters = set(i for i in formula if i in letter_set)
        if formula_letters != token_letters:
            raise Exception('Input may not be a formula; extra letters were detected')
    
    for token in tokens:
        if token == "(":
            stack.append([])
            last = stack[-1]
        elif token == ")":
            temp_dict = {}
            for d in last:
                for ele, count in d.items():
                    if ele in temp_dict:
                        temp_dict[ele] = temp_dict[ele] + count
                    else:
                        temp_dict[ele] = count
            stack.pop()
            last = stack[-1]
            last.append(temp_dict)
        elif token.isalpha():
            last.append({token: 1})
        else:
            v = float(token)
            v_int = int(v)
            if v_int == v:
                v = v_int
            last[-1] = {ele: count*v for ele, count in last[-1].items()}
    ans = {}
    for d in last:
        for ele, count in d.items():
            if ele in ans:
                ans[ele] = ans[ele] + count
            else:
                ans[ele] = count
    return ans