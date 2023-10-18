def encodeValue(self, value, toBeAdded=True):
    """Value is encoded as a sdr using the encoding parameters of the Field"""

    encodedValue = np.array(self.encoder.encode(value), dtype=realDType)

    if toBeAdded:
      self.encodings.append(encodedValue)
      self.numEncodings+=1

    return encodedValue