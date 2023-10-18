def from_spec(spec):
        """
        Creates an exploration object from a specification dict.
        """
        exploration = util.get_object(
            obj=spec,
            predefined_objects=tensorforce.core.explorations.explorations
        )
        assert isinstance(exploration, Exploration)
        return exploration