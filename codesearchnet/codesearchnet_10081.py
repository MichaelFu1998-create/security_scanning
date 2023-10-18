def cf_number_from_integer(integer):
        """
        Creates a CFNumber object from an integer

        :param integer:
            The integer to create the CFNumber for

        :return:
            A CFNumber
        """

        integer_as_long = ffi.new('long *', integer)
        return CoreFoundation.CFNumberCreate(
            CoreFoundation.kCFAllocatorDefault,
            kCFNumberCFIndexType,
            integer_as_long
        )