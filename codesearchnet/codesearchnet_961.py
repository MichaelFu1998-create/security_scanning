def _generateFirstOrder0():
  """ Generate the initial, first order, and second order transition
  probabilities for 'probability0'. For this model, we generate the following
  set of sequences:
  
    .1   .75
  0----1-----2
   \    \   
    \    \  .25
     \    \-----3
      \
       \ .9     .5 
        \--- 4--------- 2
              \
               \   .5
                \---------3   
          
  
  
  
  Parameters:
  ----------------------------------------------------------------------
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
            categoryList:  list of category names to use


  Here is an example of some return values when there are 3 categories
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
  # Initial probabilities, 'a' and 'e' equally likely
  numCategories = 5
  initProb = numpy.zeros(numCategories)
  initProb[0] = 1.0
  

  # --------------------------------------------------------------------
  # 1st order transitions
  firstOrder = dict()
  firstOrder['0'] = numpy.array([0, 0.1, 0, 0, 0.9])
  firstOrder['1'] = numpy.array([0, 0, 0.75, 0.25, 0])
  firstOrder['2'] = numpy.array([1.0, 0, 0, 0, 0])
  firstOrder['3'] = numpy.array([1.0, 0, 0, 0, 0])
  firstOrder['4'] = numpy.array([0, 0, 0.5, 0.5, 0])
   
  # --------------------------------------------------------------------
  # 2nd order transitions don't apply
  secondOrder = None
  
  # Generate the category list
  categoryList = ['%d' % x for x in range(5)]
  return (initProb, firstOrder, secondOrder, 3, categoryList)