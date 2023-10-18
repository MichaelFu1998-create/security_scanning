def getBaseSpec(cls):
    """
    Doesn't include the spatial, temporal and other parameters

    :returns: (dict) the base Spec for TMRegion.
    """
    spec = dict(
      description=TMRegion.__doc__,
      singleNodeOnly=True,
      inputs=dict(
        bottomUpIn=dict(
          description="""The input signal, conceptually organized as an
                         image pyramid data structure, but internally
                         organized as a flattened vector.""",
          dataType='Real32',
          count=0,
          required=True,
          regionLevel=False,
          isDefaultInput=True,
          requireSplitterMap=False),

        resetIn=dict(
          description="""Effectively a boolean flag that indicates whether
                         or not the input vector received in this compute cycle
                         represents the first training presentation in a
                         new temporal sequence.""",
          dataType='Real32',
          count=1,
          required=False,
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
        bottomUpOut=dict(
          description="""The output signal generated from the bottom-up inputs
                          from lower levels.""",
          dataType='Real32',
          count=0,
          regionLevel=True,
          isDefaultOutput=True),

        topDownOut=dict(
          description="""The top-down inputsignal, generated from
                        feedback from upper levels""",
          dataType='Real32',
          count=0,
          regionLevel=True,
          isDefaultOutput=False),

        activeCells=dict(
          description="The cells that are active",
          dataType='Real32',
          count=0,
          regionLevel=True,
          isDefaultOutput=False),

        predictedActiveCells=dict(
          description="The cells that are active and predicted",
          dataType='Real32',
          count=0,
          regionLevel=True,
          isDefaultOutput=False),

        anomalyScore = dict(
          description="""The score for how 'anomalous' (i.e. rare) the current
                        sequence is. Higher values are increasingly rare""",
          dataType='Real32',
          count=1,
          regionLevel=True,
          isDefaultOutput=False),

        lrnActiveStateT = dict(
          description="""Active cells during learn phase at time t.  This is
                        used for anomaly classification.""",
          dataType='Real32',
          count=0,
          regionLevel=True,
          isDefaultOutput=False),

      ),

      parameters=dict(
        breakPdb=dict(
          description='Set to 1 to stop in the pdb debugger on the next compute',
          dataType='UInt32',
          count=1,
          constraints='bool',
          defaultValue=0,
          accessMode='ReadWrite'),

        breakKomodo=dict(
          description='Set to 1 to stop in the Komodo debugger on the next compute',
          dataType='UInt32',
          count=1,
          constraints='bool',
          defaultValue=0,
          accessMode='ReadWrite'),

      ),
      commands = {}
    )

    return spec