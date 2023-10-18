def from_spec(spec, kwargs=None):
        """
        Creates a memory from a specification dict.
        """
        memory = util.get_object(
            obj=spec,
            predefined_objects=tensorforce.core.memories.memories,
            kwargs=kwargs
        )
        assert isinstance(memory, Memory)
        return memory