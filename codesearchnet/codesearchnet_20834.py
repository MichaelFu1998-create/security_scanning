def parse_asf(source, world, jointgroup=None, density=1000, color=None):
    '''Load and parse a source file.

    Parameters
    ----------
    source : file
        A file-like object that contains text information describing bodies and
        joints to add to the world.
    world : :class:`pagoda.physics.World`
        The world to add objects and joints to.
    jointgroup : ode.JointGroup, optional
        If provided, add all joints from this parse to the given group. The
        default behavior adds joints to the world without an explicit group.
    density : float, optional
        Default density for bodies. This is overridden if the source provides a
        density or mass value for a given body.
    color : tuple of floats, optional
        Default color for bodies from this source. Defaults to None, which does
        not assign a color to parsed bodies.
    '''
    visitor = AsfVisitor(world, jointgroup, density, color)
    visitor.parse(re.sub(r'#.*', ' ', source.read()))
    return visitor