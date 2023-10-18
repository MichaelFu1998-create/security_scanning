def getSpec(cls):
    """
    Overrides :meth:`nupic.bindings.regions.PyRegion.PyRegion.getSpec`.
    """
    ns = dict(
        description=KNNClassifierRegion.__doc__,
        singleNodeOnly=True,
        inputs=dict(
          categoryIn=dict(
            description='Vector of zero or more category indices for this input'
                         'sample. -1 implies no category.',
            dataType='Real32',
            count=0,
            required=True,
            regionLevel=True,
            isDefaultInput=False,
            requireSplitterMap=False),

          bottomUpIn=dict(
            description='Belief values over children\'s groups',
            dataType='Real32',
            count=0,
            required=True,
            regionLevel=False,
            isDefaultInput=True,
            requireSplitterMap=False),

          partitionIn=dict(
            description='Partition ID of the input sample',
            dataType='Real32',
            count=0,
            required=True,
            regionLevel=True,
            isDefaultInput=False,
            requireSplitterMap=False),

          auxDataIn=dict(
            description='Auxiliary data from the sensor',
            dataType='Real32',
            count=0,
            required=False,
            regionLevel=True,
            isDefaultInput=False,
            requireSplitterMap=False)
        ),


        outputs=dict(
          categoriesOut=dict(
          description='A vector representing, for each category '
                      'index, the likelihood that the input to the node belongs '
                      'to that category based on the number of neighbors of '
                      'that category that are among the nearest K.',
          dataType='Real32',
          count=0,
          regionLevel=True,
          isDefaultOutput=True),

          bestPrototypeIndices=dict(
          description='A vector that lists, in descending order of '
                      'the match, the positions of the prototypes '
                      'that best match the input pattern.',
          dataType='Real32',
          count=0,
          regionLevel=True,
          isDefaultOutput=False),

          categoryProbabilitiesOut=dict(
          description='A vector representing, for each category '
                      'index, the probability that the input to the node belongs '
                      'to that category based on the distance to the nearest '
                      'neighbor of each category.',
          dataType='Real32',
          count=0,
          regionLevel=True,
          isDefaultOutput=True),

        ),

        parameters=dict(
          learningMode=dict(
            description='Boolean (0/1) indicating whether or not a region '
                        'is in learning mode.',
            dataType='UInt32',
            count=1,
            constraints='bool',
            defaultValue=1,
            accessMode='ReadWrite'),

          inferenceMode=dict(
            description='Boolean (0/1) indicating whether or not a region '
                        'is in inference mode.',
            dataType='UInt32',
            count=1,
            constraints='bool',
            defaultValue=0,
            accessMode='ReadWrite'),

          acceptanceProbability=dict(
            description='During learning, inputs are learned with '
                        'probability equal to this parameter. '
                        'If set to 1.0, the default, '
                        'all inputs will be considered '
                        '(subject to other tests).',
            dataType='Real32',
            count=1,
            constraints='',
            defaultValue=1.0,
            #accessMode='Create'),
            accessMode='ReadWrite'), # and Create too

          confusion=dict(
            description='Confusion matrix accumulated during inference. '
                        'Reset with reset(). This is available to Python '
                        'client code only.',
            dataType='Handle',
            count=2,
            constraints='',
            defaultValue=None,
            accessMode='Read'),

          activeOutputCount=dict(
            description='The number of active elements in the '
                        '"categoriesOut" output.',
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=0,
            accessMode='Read'),

          categoryCount=dict(
            description='An integer indicating the number of '
                        'categories that have been learned',
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=None,
            accessMode='Read'),

          patternCount=dict(
            description='Number of patterns learned by the classifier.',
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=None,
            accessMode='Read'),

          patternMatrix=dict(
            description='The actual patterns learned by the classifier, '
                        'returned as a matrix.',
            dataType='Handle',
            count=1,
            constraints='',
            defaultValue=None,
            accessMode='Read'),

          k=dict(
            description='The number of nearest neighbors to use '
                        'during inference.',
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=1,
            accessMode='Create'),

          maxCategoryCount=dict(
            description='The maximal number of categories the '
                        'classifier will distinguish between.',
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=2,
            accessMode='Create'),

          distanceNorm=dict(
            description='The norm to use for a distance metric (i.e., '
                        'the "p" in Lp-norm)',
            dataType='Real32',
            count=1,
            constraints='',
            defaultValue=2.0,
            accessMode='ReadWrite'),
            #accessMode='Create'),

          distanceMethod=dict(
            description='Method used to compute distances between inputs and'
              'prototypes. Possible options are norm, rawOverlap, '
              'pctOverlapOfLarger, and pctOverlapOfProto',
            dataType="Byte",
            count=0,
            constraints='enum: norm, rawOverlap, pctOverlapOfLarger, '
              'pctOverlapOfProto, pctOverlapOfInput',
            defaultValue='norm',
            accessMode='ReadWrite'),

          outputProbabilitiesByDist=dict(
            description='If True, categoryProbabilitiesOut is the probability of '
              'each category based on the distance to the nearest neighbor of '
              'each category. If False, categoryProbabilitiesOut is the '
              'percentage of neighbors among the top K that are of each category.',
            dataType='UInt32',
            count=1,
            constraints='bool',
            defaultValue=0,
            accessMode='Create'),

          distThreshold=dict(
            description='Distance Threshold.  If a pattern that '
                        'is less than distThreshold apart from '
                        'the input pattern already exists in the '
                        'KNN memory, then the input pattern is '
                        'not added to KNN memory.',
            dataType='Real32',
            count=1,
            constraints='',
            defaultValue=0.0,
            accessMode='ReadWrite'),

          inputThresh=dict(
            description='Input binarization threshold, used if '
                        '"doBinarization" is True.',
            dataType='Real32',
            count=1,
            constraints='',
            defaultValue=0.5,
            accessMode='Create'),

          doBinarization=dict(
            description='Whether or not to binarize the input vectors.',
            dataType='UInt32',
            count=1,
            constraints='bool',
            defaultValue=0,
            accessMode='Create'),

          useSparseMemory=dict(
            description='A boolean flag that determines whether or '
                        'not the KNNClassifier will use sparse Memory',
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=1,
            accessMode='Create'),

          minSparsity=dict(
            description="If useSparseMemory is set, only vectors with sparsity"
                        " >= minSparsity will be stored during learning. A value"
                        " of 0.0 implies all vectors will be stored. A value of"
                        " 0.1 implies only vectors with at least 10% sparsity"
                        " will be stored",
            dataType='Real32',
            count=1,
            constraints='',
            defaultValue=0.0,
            accessMode='ReadWrite'),

          sparseThreshold=dict(
            description='If sparse memory is used, input variables '
                        'whose absolute value is less than this '
                        'threshold  will be stored as zero',
            dataType='Real32',
            count=1,
            constraints='',
            defaultValue=0.0,
            accessMode='Create'),

          relativeThreshold=dict(
            description='Whether to multiply sparseThreshold by max value '
                        ' in input',
            dataType='UInt32',
            count=1,
            constraints='bool',
            defaultValue=0,
            accessMode='Create'),

          winnerCount=dict(
            description='Only this many elements of the input are '
                       'stored. All elements are stored if 0.',
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=0,
            accessMode='Create'),

          doSphering=dict(
            description='A boolean indicating whether or not data should'
              'be "sphered" (i.e. each dimension should be normalized such'
              'that its mean and variance are zero and one, respectively.) This'
              ' sphering normalization would be performed after all training '
              'samples had been received but before inference was performed. '
              'The dimension-specific normalization constants would then '
              ' be applied to all future incoming vectors prior to performing '
              ' conventional NN inference.',
            dataType='UInt32',
            count=1,
            constraints='bool',
            defaultValue=0,
            accessMode='Create'),

          SVDSampleCount=dict(
            description='If not 0, carries out SVD transformation after '
                          'that many samples have been seen.',
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=0,
            accessMode='Create'),

          SVDDimCount=dict(
            description='Number of dimensions to keep after SVD if greater '
                        'than 0. If set to -1 it is considered unspecified. '
                        'If set to 0 it is consider "adaptive" and the number '
                        'is chosen automatically.',
            dataType='Int32',
            count=1,
            constraints='',
            defaultValue=-1,
            accessMode='Create'),

          fractionOfMax=dict(
            description='The smallest singular value which is retained '
                        'as a fraction of the largest singular value. This is '
                        'used only if SVDDimCount==0 ("adaptive").',
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=0,
            accessMode='Create'),

          useAuxiliary=dict(
            description='Whether or not the classifier should use auxiliary '
                        'input data.',
            dataType='UInt32',
            count=1,
            constraints='bool',
            defaultValue=0,
            accessMode='Create'),

          justUseAuxiliary=dict(
            description='Whether or not the classifier should ONLUY use the '
                        'auxiliary input data.',
            dataType='UInt32',
            count=1,
            constraints='bool',
            defaultValue=0,
            accessMode='Create'),

          verbosity=dict(
            description='An integer that controls the verbosity level, '
                        '0 means no verbose output, increasing integers '
                        'provide more verbosity.',
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=0 ,
            accessMode='ReadWrite'),

          keepAllDistances=dict(
            description='Whether to store all the protoScores in an array, '
                        'rather than just the ones for the last inference. '
                        'When this parameter is changed from True to False, '
                        'all the scores are discarded except for the most '
                        'recent one.',
            dataType='UInt32',
            count=1,
            constraints='bool',
            defaultValue=None,
            accessMode='ReadWrite'),

          replaceDuplicates=dict(
            description='A boolean flag that determines whether or'
                        'not the KNNClassifier should replace duplicates'
                        'during learning. This should be on when online'
                        'learning.',
            dataType='UInt32',
            count=1,
            constraints='bool',
            defaultValue=None,
            accessMode='ReadWrite'),

          cellsPerCol=dict(
            description='If >= 1, we assume the input is organized into columns, '
                        'in the same manner as the temporal memory AND '
                        'whenever we store a new prototype, we only store the '
                        'start cell (first cell) in any column which is bursting.'
              'colum ',
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=0,
            accessMode='Create'),

          maxStoredPatterns=dict(
            description='Limits the maximum number of the training patterns '
                        'stored. When KNN learns in a fixed capacity mode, '
                        'the unused patterns are deleted once the number '
                        'of stored patterns is greater than maxStoredPatterns'
                        'columns. [-1 is no limit] ',
            dataType='Int32',
            count=1,
            constraints='',
            defaultValue=-1,
            accessMode='Create'),
      ),
      commands=dict()
    )

    return ns