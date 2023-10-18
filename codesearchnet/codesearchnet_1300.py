def jobsGetFields(self, jobIDs, fields, requireAll=True):
    """ Fetch the values of 1 or more fields from a sequence of job records.
    Here, 'fields' is a sequence (list or tuple) with the names of the fields to
    fetch. The names are the public names of the fields (camelBack, not the
    lower_case_only form as stored in the DB).

    WARNING!!!: The order of the results are NOT necessarily in the same order as
    the order of the job IDs passed in!!!

    Parameters:
    ----------------------------------------------------------------
    jobIDs:        A sequence of jobIDs
    fields:        A list  of fields to return for each jobID

    Returns:      A list of tuples->(jobID, [field1, field2,...])
    """
    assert isinstance(jobIDs, self._SEQUENCE_TYPES)
    assert len(jobIDs) >=1

    rows = self._getMatchingRowsWithRetries(
      self._jobs, dict(job_id=jobIDs),
      ['job_id'] + [self._jobs.pubToDBNameDict[x] for x in fields])


    if requireAll and len(rows) < len(jobIDs):
      # NOTE: this will also trigger if the jobIDs list included duplicates
      raise RuntimeError("jobIDs %s not found within the jobs table" % (
        (set(jobIDs) - set(r[0] for r in rows)),))


    return [(r[0], list(r[1:])) for r in rows]