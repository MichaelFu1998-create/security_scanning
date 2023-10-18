def verify_authority(self):
        """ Verify the authority of the signed transaction
        """
        try:
            if not self.blockchain.rpc.verify_authority(self.json()):
                raise InsufficientAuthorityError
        except Exception as e:
            raise e