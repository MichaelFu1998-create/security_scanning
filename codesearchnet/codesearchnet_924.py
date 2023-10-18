def _getAdditionalSpecs(spatialImp, kwargs={}):
  """Build the additional specs in three groups (for the inspector)

  Use the type of the default argument to set the Spec type, defaulting
  to 'Byte' for None and complex types

  Determines the spatial parameters based on the selected implementation.
  It defaults to SpatialPooler.
  """
  typeNames = {int: 'UInt32', float: 'Real32', str: 'Byte', bool: 'bool', tuple: 'tuple'}

  def getArgType(arg):
    t = typeNames.get(type(arg), 'Byte')
    count = 0 if t == 'Byte' else 1
    if t == 'tuple':
      t = typeNames.get(type(arg[0]), 'Byte')
      count = len(arg)
    if t == 'bool':
      t = 'UInt32'
    return (t, count)

  def getConstraints(arg):
    t = typeNames.get(type(arg), 'Byte')
    if t == 'Byte':
      return 'multiple'
    elif t == 'bool':
      return 'bool'
    else:
      return ''

  # Get arguments from spatial pooler constructors, figure out types of
  # variables and populate spatialSpec.
  SpatialClass = getSPClass(spatialImp)
  sArgTuples = _buildArgs(SpatialClass.__init__)
  spatialSpec = {}
  for argTuple in sArgTuples:
    d = dict(
      description=argTuple[1],
      accessMode='ReadWrite',
      dataType=getArgType(argTuple[2])[0],
      count=getArgType(argTuple[2])[1],
      constraints=getConstraints(argTuple[2]))
    spatialSpec[argTuple[0]] = d

  # Add special parameters that weren't handled automatically
  # Spatial parameters only!
  spatialSpec.update(dict(

    columnCount=dict(
      description='Total number of columns (coincidences).',
      accessMode='Read',
      dataType='UInt32',
      count=1,
      constraints=''),

    inputWidth=dict(
      description='Size of inputs to the SP.',
      accessMode='Read',
      dataType='UInt32',
      count=1,
      constraints=''),

    spInputNonZeros=dict(
      description='The indices of the non-zero inputs to the spatial pooler',
      accessMode='Read',
      dataType='UInt32',
      count=0,
      constraints=''),

    spOutputNonZeros=dict(
      description='The indices of the non-zero outputs from the spatial pooler',
      accessMode='Read',
      dataType='UInt32',
      count=0,
      constraints=''),

    spOverlapDistribution=dict(
      description="""The overlaps between the active output coincidences
      and the input. The overlap amounts for each coincidence are sorted
      from highest to lowest. """,
      accessMode='Read',
      dataType='Real32',
      count=0,
      constraints=''),

    sparseCoincidenceMatrix=dict(
      description='The coincidences, as a SparseMatrix',
      accessMode='Read',
      dataType='Byte',
      count=0,
      constraints=''),

    denseOutput=dict(
      description='Score for each coincidence.',
      accessMode='Read',
      dataType='Real32',
      count=0,
      constraints=''),

    spLearningStatsStr=dict(
      description="""String representation of dictionary containing a number
                     of statistics related to learning.""",
      accessMode='Read',
      dataType='Byte',
      count=0,
      constraints='handle'),

    spatialImp=dict(
        description="""Which spatial pooler implementation to use. Set to either
                      'py', or 'cpp'. The 'cpp' implementation is optimized for
                      speed in C++.""",
        accessMode='ReadWrite',
        dataType='Byte',
        count=0,
        constraints='enum: py, cpp'),
  ))


  # The last group is for parameters that aren't specific to spatial pooler
  otherSpec = dict(
    learningMode=dict(
      description='1 if the node is learning (default 1).',
      accessMode='ReadWrite',
      dataType='UInt32',
      count=1,
      constraints='bool'),

    inferenceMode=dict(
      description='1 if the node is inferring (default 0).',
      accessMode='ReadWrite',
      dataType='UInt32',
      count=1,
      constraints='bool'),

    anomalyMode=dict(
      description='1 if an anomaly score is being computed',
      accessMode='ReadWrite',
      dataType='UInt32',
      count=1,
      constraints='bool'),

    topDownMode=dict(
      description='1 if the node should do top down compute on the next call '
                  'to compute into topDownOut (default 0).',
      accessMode='ReadWrite',
      dataType='UInt32',
      count=1,
      constraints='bool'),

    activeOutputCount=dict(
      description='Number of active elements in bottomUpOut output.',
      accessMode='Read',
      dataType='UInt32',
      count=1,
      constraints=''),

    logPathInput=dict(
      description='Optional name of input log file. If set, every input vector'
                  ' will be logged to this file.',
      accessMode='ReadWrite',
      dataType='Byte',
      count=0,
      constraints=''),

    logPathOutput=dict(
      description='Optional name of output log file. If set, every output vector'
                  ' will be logged to this file.',
      accessMode='ReadWrite',
      dataType='Byte',
      count=0,
      constraints=''),

    logPathOutputDense=dict(
      description='Optional name of output log file. If set, every output vector'
                  ' will be logged to this file as a dense vector.',
      accessMode='ReadWrite',
      dataType='Byte',
      count=0,
      constraints=''),

  )

  return spatialSpec, otherSpec