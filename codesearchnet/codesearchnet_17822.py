def extract_field(state, field='exp-particles'):
    """
    Given a state, extracts a field. Extracted value depends on the value
    of field:
        'exp-particles' : The inverted data in the regions of the particles,
                zeros otherwise -- i.e. particles + noise.
        'exp-platonic'  : Same as above, but nonzero in the region of the
                entire platonic image -- i.e. platonic + noise.
        'sim-particles' : Just the particles image; no noise from the data.
        'sim-platonic'  : Just the platonic image; no noise from the data.
    """
    es, pp = field.split('-')  #exp vs sim, particles vs platonic
    #1. The weights for the field, based off the platonic vs particles
    if pp == 'particles':
        o = state.get('obj')
        if isinstance(o, peri.comp.comp.ComponentCollection):
            wts = 0*o.get()[state.inner]
            for c in o.comps:
                if isinstance(c, peri.comp.objs.PlatonicSpheresCollection):
                    wts += c.get()[state.inner]
        else:
            wts = o.get()[state.inner]
    elif pp == 'platonic':
        wts = state.get('obj').get()[state.inner]
    else:
        raise ValueError('Not a proper field.')
    #2. Exp vs sim-like data
    if es == 'exp':
        out = (1-state.data) * (wts > 1e-5)
    elif es == 'sim':
        out = wts
    else:
        raise ValueError('Not a proper field.')
    return norm(clip(roll(out)))