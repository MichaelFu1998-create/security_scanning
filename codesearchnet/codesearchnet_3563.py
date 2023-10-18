def serialize(ty, *values, **kwargs):
        """
        Serialize value using type specification in ty.
        ABI.serialize('int256', 1000)
        ABI.serialize('(int, int256)', 1000, 2000)
        """
        try:
            parsed_ty = abitypes.parse(ty)
        except Exception as e:
            # Catch and rebrand parsing errors
            raise EthereumError(str(e))

        if parsed_ty[0] != 'tuple':
            if len(values) > 1:
                raise ValueError('too many values passed for non-tuple')
            values = values[0]
            if isinstance(values, str):
                values = values.encode()
        else:
            # implement type forgiveness for bytesM/string types
            # allow python strs also to be used for Solidity bytesM/string types
            values = tuple(val.encode() if isinstance(val, str) else val for val in values)

        result, dyn_result = ABI._serialize(parsed_ty, values)
        return result + dyn_result