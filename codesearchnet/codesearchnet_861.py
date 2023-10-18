def writeStateToDB(self):
    """Update the state in the job record with our local changes (if any).
    If we don't have the latest state in our priorStateJSON, then re-load
    in the latest state and return False. If we were successful writing out
    our changes, return True

    Parameters:
    ---------------------------------------------------------------------
    retval:    True if we were successful writing out our changes
               False if our priorState is not the latest that was in the DB.
               In this case, we will re-load our state from the DB
    """
    # If no changes, do nothing
    if not self._dirty:
      return True

    # Set the update time
    self._state['lastUpdateTime'] = time.time()
    newStateJSON = json.dumps(self._state)
    success = self._hsObj._cjDAO.jobSetFieldIfEqual(self._hsObj._jobID,
                'engWorkerState', str(newStateJSON), str(self._priorStateJSON))

    if success:
      self.logger.debug("Success changing hsState to: \n%s " % \
                       (pprint.pformat(self._state, indent=4)))
      self._priorStateJSON = newStateJSON

    # If no success, read in the current state from the DB
    else:
      self.logger.debug("Failed to change hsState to: \n%s " % \
                       (pprint.pformat(self._state, indent=4)))

      self._priorStateJSON = self._hsObj._cjDAO.jobGetFields(self._hsObj._jobID,
                                                      ['engWorkerState'])[0]
      self._state =  json.loads(self._priorStateJSON)

      self.logger.info("New hsState has been set by some other worker to: "
                       " \n%s" % (pprint.pformat(self._state, indent=4)))

    return success