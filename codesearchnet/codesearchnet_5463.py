def deserialize(cls, serializer, wf_spec, s_state, **kwargs):
        """
        Deserializes the trigger using the provided serializer.
        """
        return serializer.deserialize_trigger(wf_spec,
                                              s_state,
                                              **kwargs)