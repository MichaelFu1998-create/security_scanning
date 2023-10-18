def center_of_mass(bodies):
    '''Given a set of bodies, compute their center of mass in world coordinates.
    '''
    x = np.zeros(3.)
    t = 0.
    for b in bodies:
        m = b.mass
        x += b.body_to_world(m.c) * m.mass
        t += m.mass
    return x / t