def function_signature_for_name_and_inputs(name: str, inputs: Sequence[Mapping[str, Any]]) -> str:
        """Returns the function signature for the specified name and Solidity JSON metadata inputs array.

        The ABI specification defines the function signature as the function name followed by the parenthesised list of
        parameter types separated by single commas and no spaces.
        See https://solidity.readthedocs.io/en/latest/abi-spec.html#function-selector
        """
        return name + SolidityMetadata.tuple_signature_for_components(inputs)