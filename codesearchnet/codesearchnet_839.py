def customCompute(self, recordNum, patternNZ, classification):
    """
    Just return the inference value from one input sample. The actual
    learning happens in compute() -- if, and only if learning is enabled --
    which is called when you run the network.

    .. warning:: This method is deprecated and exists only to maintain backward 
       compatibility. This method is deprecated, and will be removed. Use 
       :meth:`nupic.engine.Network.run` instead, which will call 
       :meth:`~nupic.regions.sdr_classifier_region.compute`.

    :param recordNum: (int) Record number of the input sample.
    :param patternNZ: (list) of the active indices from the output below
    :param classification: (dict) of the classification information:
    
           * ``bucketIdx``: index of the encoder bucket
           * ``actValue``:  actual value going into the encoder

    :returns: (dict) containing inference results, one entry for each step in
              ``self.steps``. The key is the number of steps, the value is an
              array containing the relative likelihood for each ``bucketIdx``
              starting from 0.

              For example:
              
              :: 
              
                {'actualValues': [0.0, 1.0, 2.0, 3.0]
                  1 : [0.1, 0.3, 0.2, 0.7]
                  4 : [0.2, 0.4, 0.3, 0.5]}
    """

    # If the compute flag has not been initialized (for example if we
    # restored a model from an old checkpoint) initialize it to False.
    if not hasattr(self, "_computeFlag"):
      self._computeFlag = False

    if self._computeFlag:
      # Will raise an exception if the deprecated method customCompute() is
      # being used at the same time as the compute function.
      warnings.simplefilter('error', DeprecationWarning)
      warnings.warn("The customCompute() method should not be "
                    "called at the same time as the compute() "
                    "method. The compute() method is called "
                    "whenever network.run() is called.",
                    DeprecationWarning)

    return self._sdrClassifier.compute(recordNum,
                                       patternNZ,
                                       classification,
                                       self.learningMode,
                                       self.inferenceMode)