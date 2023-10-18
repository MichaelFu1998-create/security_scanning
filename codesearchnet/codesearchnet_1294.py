def jobGetModelIDs(self, jobID):
    """Fetch all the modelIDs that correspond to a given jobID; empty sequence
    if none"""

    rows = self._getMatchingRowsWithRetries(self._models, dict(job_id=jobID),
                                            ['model_id'])
    return [r[0] for r in rows]