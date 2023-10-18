def getEncoding(self, n):
    """Returns the nth encoding"""

    assert (all(field.numEncodings>n for field in self.fields))
    encoding = np.concatenate([field.encodings[n] for field in self.fields])

    return encoding