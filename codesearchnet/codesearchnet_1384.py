def drawFile(dataset, matrix, patterns, cells, w, fnum):
  '''The similarity of two patterns in the bit-encoding space is displayed alongside
  their similarity in the sp-coinc space.'''
  score=0
  count = 0
  assert len(patterns)==len(cells)
  for p in xrange(len(patterns)-1):
    matrix[p+1:,p] = [len(set(patterns[p]).intersection(set(q)))*100/w for q in patterns[p+1:]]
    matrix[p,p+1:] = [len(set(cells[p]).intersection(set(r)))*5/2 for r in cells[p+1:]]
    
    score += sum(abs(np.array(matrix[p+1:,p])-np.array(matrix[p,p+1:])))
    count += len(matrix[p+1:,p])
  
  print 'Score', score/count
  
  fig = pyl.figure(figsize = (10,10), num = fnum)
  pyl.matshow(matrix, fignum = fnum)
  pyl.colorbar()
  pyl.title('Coincidence Space', verticalalignment='top', fontsize=12)
  pyl.xlabel('The Mirror Image Visualization for '+dataset, fontsize=17)
  pyl.ylabel('Encoding space', fontsize=12)