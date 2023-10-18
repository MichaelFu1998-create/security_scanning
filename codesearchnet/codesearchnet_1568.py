def _generateFile(filename, data):
  """ 
  Parameters:
  ----------------------------------------------------------------
  filename:         name of .csv file to generate
                   
  """
  
  # Create the file
  print "Creating %s..." % (filename)
  numRecords, numFields = data.shape
  
  fields = [('field%d'%(i+1), 'float', '') for i in range(numFields)]
  outFile = File(filename, fields)
  
  for i in xrange(numRecords):
    outFile.write(data[i].tolist())
    
  outFile.close()