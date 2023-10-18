def defineField(self, name, encoderParams=None):
    """Initialize field using relevant encoder parameters.
    Parameters:
    -------------------------------------------------------------------
    name:                 Field name
    encoderParams:        Parameters for the encoder.

    Returns the index of the field
    """
    self.fields.append(_field(name, encoderParams))

    return len(self.fields)-1