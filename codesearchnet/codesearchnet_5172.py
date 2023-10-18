def get_all_certificates(self):
        """
            This function returns a list of Certificate objects.
        """
        data = self.get_data("certificates")
        certificates = list()
        for jsoned in data['certificates']:
            cert = Certificate(**jsoned)
            cert.token = self.token
            certificates.append(cert)

        return certificates