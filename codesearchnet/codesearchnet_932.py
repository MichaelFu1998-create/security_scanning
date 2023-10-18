def getSpec(cls):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.PyRegion.getSpec`.

    The parameters collection is constructed based on the parameters specified
    by the various components (spatialSpec, temporalSpec and otherSpec)
    """
    spec = cls.getBaseSpec()
    s, o = _getAdditionalSpecs(spatialImp=getDefaultSPImp())
    spec['parameters'].update(s)
    spec['parameters'].update(o)

    return spec