def _computModelDelay(self):
    """ Computes the amount of time (if any) to delay the run of this model.
    This can be determined by two mutually exclusive parameters:
    delay and sleepModelRange.

    'delay' specifies the number of seconds a model should be delayed. If a list
    is specified, the appropriate amount of delay is determined by using the
    model's modelIndex property.

    However, this doesn't work when testing orphaned models, because the
    modelIndex will be the same for every recovery attempt. Therefore, every
    recovery attempt will also be delayed and potentially orphaned.

    'sleepModelRange' doesn't use the modelIndex property for a model, but rather
    sees which order the model is in the database, and uses that to determine
    whether or not a model should be delayed.
    """

    # 'delay' and 'sleepModelRange' are mutually exclusive
    if self._params['delay'] is not None \
        and self._params['sleepModelRange'] is not None:
          raise RuntimeError("Only one of 'delay' or "
                             "'sleepModelRange' may be specified")

    # Get the sleepModel range
    if self._sleepModelRange is not None:
      range, delay = self._sleepModelRange.split(':')
      delay = float(delay)
      range = map(int, range.split(','))
      modelIDs = self._jobsDAO.jobGetModelIDs(self._jobID)
      modelIDs.sort()

      range[1] = min(range[1], len(modelIDs))

      # If the model is in range, add the delay
      if self._modelID in modelIDs[range[0]:range[1]]:
        self._delay = delay
    else:
      self._delay = self._params['delay']