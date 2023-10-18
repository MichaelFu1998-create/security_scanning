def from_spec(spec, kwargs=None):
        """
        Creates a network from a specification dict.
        """
        network = util.get_object(
            obj=spec,
            default_object=LayeredNetwork,
            kwargs=kwargs
        )
        assert isinstance(network, Network)
        return network