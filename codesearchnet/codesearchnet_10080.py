def cf_array_from_list(values):
        """
        Creates a CFArrayRef object from a list of CF* type objects.

        :param values:
            A list of CF* type object

        :return:
            A CFArrayRef
        """

        length = len(values)
        return CoreFoundation.CFArrayCreate(
            CoreFoundation.kCFAllocatorDefault,
            values,
            length,
            ffi.addressof(CoreFoundation.kCFTypeArrayCallBacks)
        )