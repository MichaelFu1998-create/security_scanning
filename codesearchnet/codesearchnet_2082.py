def from_spec(spec, kwargs=None):
        """
        Creates a layer from a specification dict.
        """
        layer = util.get_object(
            obj=spec,
            predefined_objects=tensorforce.core.networks.layers,
            kwargs=kwargs
        )
        assert isinstance(layer, Layer)
        return layer