def get_certificate(self, id):
        """
            Returns a Certificate object by its ID.

            Args:
                id (str): Certificate ID
        """
        return Certificate.get_object(api_token=self.token, cert_id=id)