def cf_number_to_number(value):
        """
        Converts a CFNumber object to a python float or integer

        :param value:
            The CFNumber object

        :return:
            A python number (float or integer)
        """

        type_ = CoreFoundation.CFNumberGetType(_cast_pointer_p(value))
        c_type = {
            1: c_byte,              # kCFNumberSInt8Type
            2: ctypes.c_short,      # kCFNumberSInt16Type
            3: ctypes.c_int32,      # kCFNumberSInt32Type
            4: ctypes.c_int64,      # kCFNumberSInt64Type
            5: ctypes.c_float,      # kCFNumberFloat32Type
            6: ctypes.c_double,     # kCFNumberFloat64Type
            7: c_byte,              # kCFNumberCharType
            8: ctypes.c_short,      # kCFNumberShortType
            9: ctypes.c_int,        # kCFNumberIntType
            10: c_long,             # kCFNumberLongType
            11: ctypes.c_longlong,  # kCFNumberLongLongType
            12: ctypes.c_float,     # kCFNumberFloatType
            13: ctypes.c_double,    # kCFNumberDoubleType
            14: c_long,             # kCFNumberCFIndexType
            15: ctypes.c_int,       # kCFNumberNSIntegerType
            16: ctypes.c_double,    # kCFNumberCGFloatType
        }[type_]
        output = c_type(0)
        CoreFoundation.CFNumberGetValue(_cast_pointer_p(value), type_, byref(output))
        return output.value