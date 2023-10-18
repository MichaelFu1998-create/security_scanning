def getSpec(cls):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.PyRegion.getSpec`.

    The parameters collection is constructed based on the parameters specified
    by the various components (spatialSpec, temporalSpec and otherSpec)
    """
    spec = cls.getBaseSpec()
    t, o = _getAdditionalSpecs(temporalImp=gDefaultTemporalImp)
    spec['parameters'].update(t)
    spec['parameters'].update(o)

    return spec