def setFlag(self, index, flag):
    """Set flag for field at index. Flags are special characters such as 'S' for
    sequence or 'T' for timestamp.
    Parameters:
    --------------------------------------------------------------------
    index:            index of field whose flag is being set
    flag:             special character
    """
    assert len(self.fields)>index
    self.fields[index].flag=flag