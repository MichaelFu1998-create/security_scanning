def _generateModel1(numCategories):
  """ Generate the initial, first order, and second order transition
  probabilities for 'model1'. For this model, we generate the following
  set of sequences:
  
  0-10-15 (1X)
  0-11-16 (1X)
  0-12-17 (1X)
  0-13-18 (1X)
  0-14-19 (1X)

  1-10-20 (1X)
  1-11-21 (1X)
  1-12-22 (1X)
  1-13-23 (1X)
  1-14-24 (1X)
  
  
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


  # --------------------------------------------------------------------
  # Initial probabilities, 0 and 1 equally likely
  initProb = numpy.zeros(numCategories)
  initProb[0] = 0.5
  initProb[1] = 0.5
  

  # --------------------------------------------------------------------
  # 1st order transitions
  # both 0 and 1 should lead to 10,11,12,13,14 with equal probability
  firstOrder = dict()
  for catIdx in range(numCategories):
    key = str([catIdx])
    probs = numpy.ones(numCategories) / numCategories
    if catIdx == 0 or catIdx == 1:
      indices = numpy.array([10,11,12,13,14])
      probs.fill(0)
      probs[indices] = 1.0    # lead only to b
      probs /= probs.sum()
    firstOrder[key] = probs
   
  # --------------------------------------------------------------------
  # 2nd order transitions
  # 0-10 should lead to 15
  # 0-11 to 16
  # ...
  # 1-10 should lead to 20
  # 1-11 shold lean to 21
  # ...
  secondOrder = dict()
  for firstIdx in range(numCategories):
    for secondIdx in range(numCategories):
      key = str([firstIdx, secondIdx])
      probs = numpy.ones(numCategories) / numCategories
      if key == str([0,10]):
        probs.fill(0)
        probs[15] = 1
      elif key == str([0,11]):
        probs.fill(0)
        probs[16] = 1
      elif key == str([0,12]):
        probs.fill(0)
        probs[17] = 1
      elif key == str([0,13]):
        probs.fill(0)
        probs[18] = 1
      elif key == str([0,14]):
        probs.fill(0)
        probs[19] = 1
    
      elif key == str([1,10]):
        probs.fill(0)
        probs[20] = 1
      elif key == str([1,11]):
        probs.fill(0)
        probs[21] = 1
      elif key == str([1,12]):
        probs.fill(0)
        probs[22] = 1
      elif key == str([1,13]):
        probs.fill(0)
        probs[23] = 1
      elif key == str([1,14]):
        probs.fill(0)
        probs[24] = 1
    
      secondOrder[key] = probs
  
  return (initProb, firstOrder, secondOrder, 3)