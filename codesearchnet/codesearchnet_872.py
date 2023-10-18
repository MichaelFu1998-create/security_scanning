def addEncoder(self, name, encoder):
    """
    Adds one encoder.

    :param name: (string) name of encoder, should be unique
    :param encoder: (:class:`.Encoder`) the encoder to add
    """
    self.encoders.append((name, encoder, self.width))
    for d in encoder.getDescription():
      self.description.append((d[0], d[1] + self.width))
    self.width += encoder.getWidth()