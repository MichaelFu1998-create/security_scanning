def constructor_abi(self) -> Dict[str, Any]:
        """Returns a copy of the Solidity JSON ABI item for the contract constructor.

        The content of the returned dict is described at https://solidity.readthedocs.io/en/latest/abi-spec.html#json_
        """
        item = self._constructor_abi_item
        if item:
            return dict(item)
        return {'inputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}