def assert_penaltymodel_factory_available():
    """For `dwavebinarycsp` to be functional, at least one penalty model factory
    has to be installed. See discussion in setup.py for details.
    """

    from pkg_resources import iter_entry_points
    from penaltymodel.core import FACTORY_ENTRYPOINT
    from itertools import chain

    supported = ('maxgap', 'mip')
    factories = chain(*(iter_entry_points(FACTORY_ENTRYPOINT, name) for name in supported))

    try:
        next(factories)
    except StopIteration:
        raise AssertionError(
            "To use 'dwavebinarycsp', at least one penaltymodel factory must be installed. "
            "Try {}.".format(
                " or ".join("'pip install dwavebinarycsp[{}]'".format(name) for name in supported)
            ))