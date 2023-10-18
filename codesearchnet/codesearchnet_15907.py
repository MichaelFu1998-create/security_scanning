def to_pointer(cls, instance):
        """Get a pointer to the private object.
        """
        return OctavePtr(instance._ref, instance._name, instance._address)