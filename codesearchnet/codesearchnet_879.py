def __validateExperimentControl(self, control):
    """ Validates control dictionary for the experiment context"""
    # Validate task list
    taskList = control.get('tasks', None)
    if taskList is not None:
      taskLabelsList = []

      for task in taskList:
        validateOpfJsonValue(task, "opfTaskSchema.json")
        validateOpfJsonValue(task['taskControl'], "opfTaskControlSchema.json")

        taskLabel = task['taskLabel']

        assert isinstance(taskLabel, types.StringTypes), \
               "taskLabel type: %r" % type(taskLabel)
        assert len(taskLabel) > 0, "empty string taskLabel not is allowed"

        taskLabelsList.append(taskLabel.lower())

      taskLabelDuplicates = filter(lambda x: taskLabelsList.count(x) > 1,
                                   taskLabelsList)
      assert len(taskLabelDuplicates) == 0, \
             "Duplcate task labels are not allowed: %s" % taskLabelDuplicates

    return