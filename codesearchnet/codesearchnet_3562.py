def function_call(type_spec, *args):
        """
        Build transaction data from function signature and arguments
        """
        m = re.match(r"(?P<name>[a-zA-Z_][a-zA-Z_0-9]*)(?P<type>\(.*\))", type_spec)
        if not m:
            raise EthereumError("Function signature expected")

        ABI._check_and_warn_num_args(type_spec, *args)

        result = ABI.function_selector(type_spec)  # Funcid
        result += ABI.serialize(m.group('type'), *args)
        return result