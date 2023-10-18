def from_value(cls, value):
        """This is how an instance is created when we read a
           MatlabObject from a MAT file.
        """
        instance = OctaveUserClass.__new__(cls)
        instance._address = '%s_%s' % (instance._name, id(instance))
        instance._ref().push(instance._address, value)
        return instance