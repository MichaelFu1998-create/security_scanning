def perm(lst, func):
    ''' Produce permutations of `lst`, where permutations are mutated by `func`. Used for flipping constraints. highly
    possible that returned constraints can be unsat this does it blindly, without any attention to the constraints
    themselves

    Considering lst as a list of constraints, e.g.

      [ C1, C2, C3 ]

    we'd like to consider scenarios of all possible permutations of flipped constraints, excluding the original list.
    So we'd like to generate:

      [ func(C1),      C2 ,       C3 ],
      [      C1 , func(C2),       C3 ],
      [ func(C1), func(C2),       C3 ],
      [      C1 ,      C2 ,  func(C3)],
      .. etc

    This is effectively treating the list of constraints as a bitmask of width len(lst) and counting up, skipping the
    0th element (unmodified array).

    The code below yields lists of constraints permuted as above by treating list indeces as bitmasks from 1 to
     2**len(lst) and applying func to all the set bit offsets.

    '''
    for i in range(1, 2**len(lst)):
        yield [func(item) if (1<<j)&i else item for (j, item) in enumerate(lst)]