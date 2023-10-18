def getZeroedOutEncoding(self, n):
    """Returns the nth encoding with the predictedField zeroed out"""

    assert all(field.numRecords>n for field in self.fields)

    encoding = np.concatenate([field.encoder.encode(SENTINEL_VALUE_FOR_MISSING_DATA)\
        if field.isPredictedField else field.encodings[n] for field in self.fields])

    return encoding