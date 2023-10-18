def getSpec(cls):
    """
    Overrides :meth:`nupic.bindings.regions.PyRegion.PyRegion.getSpec`.
    """
    ns = dict(
      description=SDRClassifierRegion.__doc__,
      singleNodeOnly=True,

      inputs=dict(
        actValueIn=dict(
          description="Actual value of the field to predict. Only taken "
                      "into account if the input has no category field.",
          dataType="Real32",
          count=0,
          required=False,
          regionLevel=False,
          isDefaultInput=False,
          requireSplitterMap=False),

        bucketIdxIn=dict(
          description="Active index of the encoder bucket for the "
                      "actual value of the field to predict. Only taken "
                      "into account if the input has no category field.",
          dataType="UInt64",
          count=0,
          required=False,
          regionLevel=False,
          isDefaultInput=False,
          requireSplitterMap=False),

        categoryIn=dict(
          description='Vector of categories of the input sample',
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

        predictedActiveCells=dict(
          description="The cells that are active and predicted",
          dataType='Real32',
          count=0,
          required=True,
          regionLevel=True,
          isDefaultInput=False,
          requireSplitterMap=False),

        sequenceIdIn=dict(
          description="Sequence ID",
          dataType='UInt64',
          count=1,
          required=False,
          regionLevel=True,
          isDefaultInput=False,
          requireSplitterMap=False),
      ),

      outputs=dict(
        categoriesOut=dict(
          description='Classification results',
          dataType='Real32',
          count=0,
          regionLevel=True,
          isDefaultOutput=False,
          requireSplitterMap=False),

        actualValues=dict(
          description='Classification results',
          dataType='Real32',
          count=0,
          regionLevel=True,
          isDefaultOutput=False,
          requireSplitterMap=False),

        probabilities=dict(
          description='Classification results',
          dataType='Real32',
          count=0,
          regionLevel=True,
          isDefaultOutput=False,
          requireSplitterMap=False),
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

        maxCategoryCount=dict(
          description='The maximal number of categories the '
                      'classifier will distinguish between.',
          dataType='UInt32',
          required=True,
          count=1,
          constraints='',
          # arbitrarily large value
          defaultValue=2000,
          accessMode='Create'),

        steps=dict(
          description='Comma separated list of the desired steps of '
                      'prediction that the classifier should learn',
          dataType="Byte",
          count=0,
          constraints='',
          defaultValue='0',
          accessMode='Create'),

        alpha=dict(
          description='The alpha is the learning rate of the classifier.'
                      'lower alpha results in longer term memory and slower '
                      'learning',
          dataType="Real32",
          count=1,
          constraints='',
          defaultValue=0.001,
          accessMode='Create'),

        implementation=dict(
          description='The classifier implementation to use.',
          accessMode='ReadWrite',
          dataType='Byte',
          count=0,
          constraints='enum: py, cpp'),

        verbosity=dict(
          description='An integer that controls the verbosity level, '
                      '0 means no verbose output, increasing integers '
                      'provide more verbosity.',
          dataType='UInt32',
          count=1,
          constraints='',
          defaultValue=0,
          accessMode='ReadWrite'),
      ),
      commands=dict()
    )

    return ns