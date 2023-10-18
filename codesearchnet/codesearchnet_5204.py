def get_object(cls, api_token, cert_id):
        """
            Class method that will return a Certificate object by its ID.
        """
        certificate = cls(token=api_token, id=cert_id)
        certificate.load()
        return certificate