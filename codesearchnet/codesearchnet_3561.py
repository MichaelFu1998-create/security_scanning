def _type_size(ty):
        """ Calculate `static` type size """
        if ty[0] in ('int', 'uint', 'bytesM', 'function'):
            return 32
        elif ty[0] in ('tuple'):
            result = 0
            for ty_i in ty[1]:
                result += ABI._type_size(ty_i)
            return result
        elif ty[0] in ('array'):
            rep = ty[1]
            result = 32  # offset link
            return result
        elif ty[0] in ('bytes', 'string'):
            result = 32  # offset link
            return result
        raise ValueError