def getBaseSpec(cls):
    """
    Doesn't include the spatial, temporal and other parameters

    :returns: (dict) The base Spec for SPRegion.
    """
    spec = dict(
      description=SPRegion.__doc__,
      singleNodeOnly=True,
      inputs=dict(
        bottomUpIn=dict(
          description="""The input vector.""",
          dataType='Real32',
          count=0,
          required=True,
          regionLevel=False,
          isDefaultInput=True,
          requireSplitterMap=False),

        resetIn=dict(
          description="""A boolean flag that indicates whether
                         or not the input vector received in this compute cycle
                         represents the start of a new temporal sequence.""",
          dataType='Real32',
          count=1,
          required=False,
          regionLevel=True,
          isDefaultInput=False,
          requireSplitterMap=False),

        topDownIn=dict(
          description="""The top-down input signal, generated from
                        feedback from upper levels""",
          dataType='Real32',
          count=0,
          required = False,
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
          description="""The top-down output signal, generated from
                        feedback from upper levels""",
          dataType='Real32',
          count=0,
          regionLevel=True,
          isDefaultOutput=False),

        spatialTopDownOut = dict(
          description="""The top-down output, generated only from the current
                         SP output. This can be used to evaluate how well the
                         SP is representing the inputs independent of the TM.""",
          dataType='Real32',
          count=0,
          regionLevel=True,
          isDefaultOutput=False),

        temporalTopDownOut = dict(
          description="""The top-down output, generated only from the current
                         TM output feedback down through the SP.""",
          dataType='Real32',
          count=0,
          regionLevel=True,
          isDefaultOutput=False),

        anomalyScore = dict(
          description="""The score for how 'anomalous' (i.e. rare) this spatial
                        input pattern is. Higher values are increasingly rare""",
          dataType='Real32',
          count=1,
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
    )

    return spec