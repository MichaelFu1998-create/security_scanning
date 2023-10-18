def optimize_particle(state, index, method='gn', doradius=True):
    """
    Methods available are
        gn : Gauss-Newton with JTJ (recommended)
        nr : Newton-Rhaphson with hessian

    if doradius, also optimize the radius.
    """
    blocks = state.param_particle(index)

    if not doradius:
        blocks = blocks[:-1]

    g = state.gradloglikelihood(blocks=blocks)
    if method == 'gn':
        h = state.jtj(blocks=blocks)
    if method == 'nr':
        h = state.hessloglikelihood(blocks=blocks)
    step = np.linalg.solve(h, g)

    h = np.zeros_like(g)
    for i in range(len(g)):
        state.update(blocks[i], state.state[blocks[i]] - step[i])
    return g,h