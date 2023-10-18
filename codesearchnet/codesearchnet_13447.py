def from_file(cls, filename):
        """Load certificate from a file.
        """
        with open(filename, "r") as pem_file:
            data = pem.readPemFromFile(pem_file)
        return cls.from_der_data(data)