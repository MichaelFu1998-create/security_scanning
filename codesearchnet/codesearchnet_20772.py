def write_table_pair_potential(func, dfunc=None, bounds=(1.0, 10.0), samples=1000, tollerance=1e-6, keyword='PAIR'):
    """A helper function to write lammps pair potentials to string. Assumes that
    functions are vectorized.

    Parameters
    ----------
    func: function
       A function that will be evaluated for the force at each radius. Required to
       be numpy vectorizable.
    dfunc: function
       Optional. A function that will be evaluated for the energy at each
       radius. If not supplied the centered difference method will be
       used. Required to be numpy vectorizable.
    bounds: tuple, list
       Optional. specifies min and max radius to evaluate the
       potential. Default 1 length unit, 10 length unit.
    samples: int
       Number of points to evaluate potential. Default 1000. Note that
       a low number of sample points will reduce accuracy.
    tollerance: float
       Value used to centered difference differentiation.
    keyword: string
       Lammps keyword to use to pair potential. This keyword will need
       to be used in the lammps pair_coeff. Default ``PAIR``
    filename: string
       Optional. filename to write lammps table potential as. Default
       ``lammps.table`` it is highly recomended to change the value.

    A file for each unique pair potential is required.
    """
    r_min, r_max = bounds
    if dfunc is None:
        dfunc = lambda r: (func(r+tollerance) - func(r-tollerance)) / (2*tollerance)

    i = np.arange(1, samples+1)
    r = np.linspace(r_min, r_max, samples)
    forces = func(r)
    energies = dfunc(r)
    lines = ['%d %f %f %f\n' % (index, radius, force, energy) for index, radius, force, energy in zip(i, r, forces, energies)]
    return "%s\nN %d\n\n" % (keyword, samples) + ''.join(lines)