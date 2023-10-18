def cf_number_to_number(value):
        """
        Converts a CFNumber object to a python float or integer

        :param value:
            The CFNumber object

        :return:
            A python number (float or integer)
        """

        type_ = CoreFoundation.CFNumberGetType(value)
        type_name_ = {
            1: 'int8_t',      # kCFNumberSInt8Type
            2: 'in16_t',      # kCFNumberSInt16Type
            3: 'int32_t',     # kCFNumberSInt32Type
            4: 'int64_t',     # kCFNumberSInt64Type
            5: 'float',       # kCFNumberFloat32Type
            6: 'double',      # kCFNumberFloat64Type
            7: 'char',        # kCFNumberCharType
            8: 'short',       # kCFNumberShortType
            9: 'int',         # kCFNumberIntType
            10: 'long',       # kCFNumberLongType
            11: 'long long',  # kCFNumberLongLongType
            12: 'float',      # kCFNumberFloatType
            13: 'double',     # kCFNumberDoubleType
            14: 'long',       # kCFNumberCFIndexType
            15: 'int',        # kCFNumberNSIntegerType
            16: 'double',     # kCFNumberCGFloatType
        }[type_]
        output = new(CoreFoundation, type_name_ + ' *')
        CoreFoundation.CFNumberGetValue(value, type_, output)
        return deref(output)