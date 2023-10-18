def getSpec(cls):
    """
    Overrides :meth:`nupic.bindings.regions.PyRegion.PyRegion.getSpec`.
    """
    ns = dict(
        description=KNNAnomalyClassifierRegion.__doc__,
        singleNodeOnly=True,
        inputs=dict(
          spBottomUpOut=dict(
            description="""The output signal generated from the bottom-up inputs
                            from lower levels.""",
            dataType='Real32',
            count=0,
            required=True,
            regionLevel=False,
            isDefaultInput=True,
            requireSplitterMap=False),

          tpTopDownOut=dict(
            description="""The top-down inputsignal, generated from
                          feedback from upper levels""",
            dataType='Real32',
            count=0,
            required=True,
            regionLevel=False,
            isDefaultInput=True,
            requireSplitterMap=False),

          tpLrnActiveStateT=dict(
            description="""Active cells in the learn state at time T from TM.
                        This is used to classify on.""",
            dataType='Real32',
            count=0,
            required=True,
            regionLevel=False,
            isDefaultInput=True,
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
        ),

        parameters=dict(
          trainRecords=dict(
            description='Number of records to wait for training',
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=0,
            accessMode='Create'),

          anomalyThreshold=dict(
            description='Threshold used to classify anomalies.',
            dataType='Real32',
            count=1,
            constraints='',
            defaultValue=0,
            accessMode='Create'),

          cacheSize=dict(
            description='Number of records to store in cache.',
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=0,
            accessMode='Create'),

          classificationVectorType=dict(
            description="""Vector type to use when classifying.
              1 - Vector Column with Difference (TM and SP)
            """,
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=1,
            accessMode='ReadWrite'),

          activeColumnCount=dict(
            description="""Number of active columns in a given step. Typically
            equivalent to SP.numActiveColumnsPerInhArea""",
            dataType='UInt32',
            count=1,
            constraints='',
            defaultValue=40,
            accessMode='ReadWrite'),

          classificationMaxDist=dict(
            description="""Maximum distance a sample can be from an anomaly
            in the classifier to be labeled as an anomaly.

            Ex: With rawOverlap distance, a value of 0.65 means that the points
            must be at most a distance 0.65 apart from each other. This
            translates to they must be at least 35% similar.""",
            dataType='Real32',
            count=1,
            constraints='',
            defaultValue=0.65,
            accessMode='Create'
            )
        ),
        commands=dict(
          getLabels=dict(description=
            "Returns a list of label dicts with properties ROWID and labels."
            "ROWID corresponds to the records id and labels is a list of "
            "strings representing the records labels.  Takes additional "
            "integer properties start and end representing the range that "
            "will be returned."),

          addLabel=dict(description=
            "Takes parameters start, end and labelName. Adds the label "
            "labelName to the records from start to end. This will recalculate "
            "labels from end to the most recent record."),

          removeLabels=dict(description=
            "Takes additional parameters start, end, labelFilter.  Start and "
            "end correspond to range to remove the label. Remove labels from "
            "each record with record ROWID in range from start to end, "
            "noninclusive of end. Removes all records if labelFilter is None, "
            "otherwise only removes the labels eqaul to labelFilter.")
        )
      )

    ns['parameters'].update(KNNClassifierRegion.getSpec()['parameters'])

    return ns