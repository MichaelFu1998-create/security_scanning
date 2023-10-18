def _getAdditionalSpecs(temporalImp, kwargs={}):
  """Build the additional specs in three groups (for the inspector)

  Use the type of the default argument to set the Spec type, defaulting
  to 'Byte' for None and complex types

  Determines the spatial parameters based on the selected implementation.
  It defaults to TemporalMemory.
  Determines the temporal parameters based on the temporalImp
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

  # Build up parameters from temporal memory's constructor
  TemporalClass = _getTPClass(temporalImp)
  tArgTuples = _buildArgs(TemporalClass.__init__)
  temporalSpec = {}
  for argTuple in tArgTuples:
    d = dict(
      description=argTuple[1],
      accessMode='ReadWrite',
      dataType=getArgType(argTuple[2])[0],
      count=getArgType(argTuple[2])[1],
      constraints=getConstraints(argTuple[2]))
    temporalSpec[argTuple[0]] = d

  # Add temporal parameters that weren't handled automatically
  temporalSpec.update(dict(
    columnCount=dict(
      description='Total number of columns.',
      accessMode='Read',
      dataType='UInt32',
      count=1,
      constraints=''),

    cellsPerColumn=dict(
      description='Number of cells per column.',
      accessMode='Read',
      dataType='UInt32',
      count=1,
      constraints=''),

    inputWidth=dict(
      description='Number of inputs to the TM.',
      accessMode='Read',
      dataType='UInt32',
      count=1,
      constraints=''),

    predictedSegmentDecrement=dict(
      description='Predicted segment decrement',
      accessMode='Read',
      dataType='Real',
      count=1,
      constraints=''),

    orColumnOutputs=dict(
      description="""OR together the cell outputs from each column to produce
      the temporal memory output. When this mode is enabled, the number of
      cells per column must also be specified and the output size of the region
      should be set the same as columnCount""",
      accessMode='Read',
      dataType='Bool',
      count=1,
      constraints='bool'),

    cellsSavePath=dict(
      description="""Optional path to file in which large temporal memory cells
                     data structure is to be saved.""",
      accessMode='ReadWrite',
      dataType='Byte',
      count=0,
      constraints=''),

    temporalImp=dict(
      description="""Which temporal memory implementation to use. Set to either
       'py' or 'cpp'. The 'cpp' implementation is optimized for speed in C++.""",
      accessMode='ReadWrite',
      dataType='Byte',
      count=0,
      constraints='enum: py, cpp'),

  ))

  # The last group is for parameters that aren't strictly spatial or temporal
  otherSpec = dict(
    learningMode=dict(
      description='True if the node is learning (default True).',
      accessMode='ReadWrite',
      dataType='Bool',
      count=1,
      defaultValue=True,
      constraints='bool'),

    inferenceMode=dict(
      description='True if the node is inferring (default False).',
      accessMode='ReadWrite',
      dataType='Bool',
      count=1,
      defaultValue=False,
      constraints='bool'),

    computePredictedActiveCellIndices=dict(
      description='True if active and predicted active indices should be computed',
      accessMode='Create',
      dataType='Bool',
      count=1,
      defaultValue=False,
      constraints='bool'),

    anomalyMode=dict(
      description='True if an anomaly score is being computed',
      accessMode='Create',
      dataType='Bool',
      count=1,
      defaultValue=False,
      constraints='bool'),

    topDownMode=dict(
      description='True if the node should do top down compute on the next call '
                  'to compute into topDownOut (default False).',
      accessMode='ReadWrite',
      dataType='Bool',
      count=1,
      defaultValue=False,
      constraints='bool'),

    activeOutputCount=dict(
      description='Number of active elements in bottomUpOut output.',
      accessMode='Read',
      dataType='UInt32',
      count=1,
      constraints=''),

    storeDenseOutput=dict(
      description="""Whether to keep the dense column output (needed for
                     denseOutput parameter).""",
      accessMode='ReadWrite',
      dataType='UInt32',
      count=1,
      constraints='bool'),

    logPathOutput=dict(
      description='Optional name of output log file. If set, every output vector'
                  ' will be logged to this file as a sparse vector.',
      accessMode='ReadWrite',
      dataType='Byte',
      count=0,
      constraints=''),

  )

  return temporalSpec, otherSpec