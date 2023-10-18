def convertNupicEnvToOPF(self):
    """
    TODO: document
    """

    # We need to create a task structure, most of which is taken verbatim
    # from the Nupic control dict
    task = dict(self.__control)

    task.pop('environment')
    inferenceArgs = task.pop('inferenceArgs')
    task['taskLabel'] = 'DefaultTask'

    # Create the iterationCycle element that will be placed inside the
    #  taskControl.
    iterationCount = task.get('iterationCount', -1)
    iterationCountInferOnly = task.pop('iterationCountInferOnly', 0)
    if iterationCountInferOnly == -1:
      iterationCycle = [IterationPhaseSpecInferOnly(1000, inferenceArgs=inferenceArgs)]
    elif iterationCountInferOnly > 0:
      assert iterationCount > 0, "When iterationCountInferOnly is specified, "\
        "iterationCount must also be specified and not be -1"
      iterationCycle = [IterationPhaseSpecLearnAndInfer(iterationCount
                                                    -iterationCountInferOnly, inferenceArgs=inferenceArgs),
                        IterationPhaseSpecInferOnly(iterationCountInferOnly, inferenceArgs=inferenceArgs)]
    else:
      iterationCycle = [IterationPhaseSpecLearnAndInfer(1000, inferenceArgs=inferenceArgs)]


    taskControl = dict(metrics = task.pop('metrics'),
                       loggedMetrics = task.pop('loggedMetrics'),
                       iterationCycle = iterationCycle)
    task['taskControl'] = taskControl

    # Create the new control
    self.__control = dict(environment = OpfEnvironment.Nupic,
                          tasks = [task])