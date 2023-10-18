def to_dict(self, mevm):
        """
        Only meant to be used with concrete Transaction objects! (after calling .concretize())
        """
        return dict(type=self.sort,
                    from_address=self.caller,
                    from_name=mevm.account_name(self.caller),
                    to_address=self.address,
                    to_name=mevm.account_name(self.address),
                    value=self.value,
                    gas=self.gas,
                    data=binascii.hexlify(self.data).decode())