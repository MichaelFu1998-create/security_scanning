def getAllEncodings(self):
    """Returns encodings for all the records"""

    numEncodings=self.fields[0].numEncodings
    assert (all(field.numEncodings==numEncodings for field in self.fields))
    encodings = [self.getEncoding(index) for index in range(numEncodings)]

    return encodings