def getSDRforValue(self, i, j):
    """Returns the sdr for jth value at column i"""
    assert len(self.fields)>i
    assert self.fields[i].numRecords>j
    encoding = self.fields[i].encodings[j]

    return encoding