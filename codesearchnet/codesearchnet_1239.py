def _generateModel2(numCategories, alpha=0.25):
  """ Generate the initial, first order, and second order transition
  probabilities for 'model2'. For this model, we generate peaked random 
  transitions using dirichlet distributions. 
  
  Parameters:
  ----------------------------------------------------------------------
  numCategories:      Number of categories
  alpha:              Determines the peakedness of the transitions. Low alpha 
                      values (alpha=0.01) place the entire weight on a single 
                      transition. Large alpha values (alpha=10) distribute the 
                      evenly among all transitions. Intermediate values (alpha=0.5)
                      give a moderately peaked transitions. 
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
                          elements by the secondOrder table. None means infinite
                          length. 


  Here is an example of some return values for an intermediate alpha value:
  initProb:         [0.33, 0.33, 0.33]
  
  firstOrder:       {'[0]': [0.2, 0.7, 0.1],
                     '[1]': [0.1, 0.1, 0.8],
                     '[2]': [0.1, 0.0, 0.9]}
                     
  secondOrder:      {'[0,0]': [0.1, 0.0, 0.9],
                     '[0,1]': [0.0, 0.2, 0.8],
                     '[0,2]': [0.1, 0.8, 0.1],
                     ...
                     '[2,2]': [0.8, 0.2, 0.0]}
  """


  # --------------------------------------------------------------------
  # All initial probabilities, are equally likely
  initProb = numpy.ones(numCategories)/numCategories

  def generatePeakedProbabilities(lastIdx,
				  numCategories=numCategories, 
				  alpha=alpha):
    probs = numpy.random.dirichlet(alpha=[alpha]*numCategories)
    probs[lastIdx] = 0.0
    probs /= probs.sum()
    return probs 

  # --------------------------------------------------------------------
  # 1st order transitions
  firstOrder = dict()
  for catIdx in range(numCategories):
    key = str([catIdx])
    probs = generatePeakedProbabilities(catIdx) 
    firstOrder[key] = probs

  # --------------------------------------------------------------------
  # 2nd order transitions
  secondOrder = dict()
  for firstIdx in range(numCategories):
    for secondIdx in range(numCategories):
      key = str([firstIdx, secondIdx])
      probs = generatePeakedProbabilities(secondIdx) 
      secondOrder[key] = probs

  return (initProb, firstOrder, secondOrder, None)