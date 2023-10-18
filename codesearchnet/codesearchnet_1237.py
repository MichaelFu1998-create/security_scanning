def _generateModel0(numCategories):
  """ Generate the initial, first order, and second order transition
  probabilities for 'model0'. For this model, we generate the following
  set of sequences:
  
  1-2-3   (4X)
  1-2-4   (1X)
  5-2-3   (1X)
  5-2-4   (4X)
  
  
  Parameters:
  ----------------------------------------------------------------------
  numCategories:      Number of categories
  retval: (initProb, firstOrder, secondOrder, seqLen)
            initProb:     Initial probability for each category. This is a vector
                            of length len(categoryList).
            firstOrder:   A dictionary of the 1st order probabilities. The key
                            is the 1st element of the sequence, the value is
                            the probability of each 2nd element given the first. 
            secondOrder:  A dictionary of the 2nd order probabilities. The key
                            is the first 2 elements of the sequence, the value is
                            the probability of each possible 3rd element given the 
                            first two. 
            seqLen:       Desired length of each sequence. The 1st element will
                          be generated using the initProb, the 2nd element by the
                          firstOrder table, and the 3rd and all successive 
                          elements by the secondOrder table. 


  Here is an example of some return values:
  initProb:         [0.7, 0.2, 0.1]
  
  firstOrder:       {'[0]': [0.3, 0.3, 0.4],
                     '[1]': [0.3, 0.3, 0.4],
                     '[2]': [0.3, 0.3, 0.4]}
                     
  secondOrder:      {'[0,0]': [0.3, 0.3, 0.4],
                     '[0,1]': [0.3, 0.3, 0.4],
                     '[0,2]': [0.3, 0.3, 0.4],
                     '[1,0]': [0.3, 0.3, 0.4],
                     '[1,1]': [0.3, 0.3, 0.4],
                     '[1,2]': [0.3, 0.3, 0.4],
                     '[2,0]': [0.3, 0.3, 0.4],
                     '[2,1]': [0.3, 0.3, 0.4],
                     '[2,2]': [0.3, 0.3, 0.4]}
  """

  # ===============================================================
  # Let's model the following:
  #  a-b-c (4X)
  #  a-b-d (1X)
  #  e-b-c (1X)
  #  e-b-d (4X)


  # --------------------------------------------------------------------
  # Initial probabilities, 'a' and 'e' equally likely
  initProb = numpy.zeros(numCategories)
  initProb[0] = 0.5
  initProb[4] = 0.5
  

  # --------------------------------------------------------------------
  # 1st order transitions
  # both 'a' and 'e' should lead to 'b'
  firstOrder = dict()
  for catIdx in range(numCategories):
    key = str([catIdx])
    probs = numpy.ones(numCategories) / numCategories
    if catIdx == 0 or catIdx == 4:
      probs.fill(0)
      probs[1] = 1.0    # lead only to b
    firstOrder[key] = probs
   
  # --------------------------------------------------------------------
  # 2nd order transitions
  # a-b should lead to c 80% and d 20%
  # e-b should lead to c 20% and d 80%
  secondOrder = dict()
  for firstIdx in range(numCategories):
    for secondIdx in range(numCategories):
      key = str([firstIdx, secondIdx])
      probs = numpy.ones(numCategories) / numCategories
      if key == str([0,1]):
        probs.fill(0)
        probs[2] = 0.80   # 'ab' leads to 'c' 80% of the time
        probs[3] = 0.20   # 'ab' leads to 'd' 20% of the time
      elif key == str([4,1]):
        probs.fill(0)
        probs[2] = 0.20   # 'eb' leads to 'c' 20% of the time
        probs[3] = 0.80   # 'eb' leads to 'd' 80% of the time
    
      secondOrder[key] = probs
  
  return (initProb, firstOrder, secondOrder, 3)