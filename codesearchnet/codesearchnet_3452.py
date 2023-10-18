def flip(constraint):
    '''
    flips a constraint (Equal)

    (Equal (BitVecITE Cond IfC ElseC) IfC)
        ->
    (Equal (BitVecITE Cond IfC ElseC) ElseC)
    '''
    equal = copy.copy(constraint)

    assert len(equal.operands) == 2
    # assume they are the equal -> ite form that we produce on standard branches
    ite, forcepc = equal.operands
    assert isinstance(ite, BitVecITE) and isinstance(forcepc, BitVecConstant)
    assert len(ite.operands) == 3
    cond, iifpc, eelsepc = ite.operands
    assert isinstance(iifpc, BitVecConstant) and isinstance(eelsepc, BitVecConstant)

    equal._operands= (equal.operands[0], eelsepc if forcepc.value == iifpc.value else iifpc)

    return equal