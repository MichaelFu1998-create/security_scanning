def saveRecords(self, path='myOutput'):
    """Export all the records into a csv file in numenta format.

    Example header format:
    fieldName1    fieldName2    fieldName3
    date          string        float
    T             S

    Parameters:
    --------------------------------------------------------------------
    path:      Relative path of the file to which the records are to be exported
    """
    numRecords = self.fields[0].numRecords
    assert (all(field.numRecords==numRecords for field in self.fields))

    import csv
    with open(path+'.csv', 'wb') as f:
      writer = csv.writer(f)
      writer.writerow(self.getAllFieldNames())
      writer.writerow(self.getAllDataTypes())
      writer.writerow(self.getAllFlags())
      writer.writerows(self.getAllRecords())
    if self.verbosity>0:
      print '******', numRecords,'records exported in numenta format to file:',\
                path,'******\n'