def jobGetFields(self, jobID, fields):
    """ Fetch the values of 1 or more fields from a job record. Here, 'fields'
    is a list with the names of the fields to fetch. The names are the public
    names of the fields (camelBack, not the lower_case_only form as stored in
    the DB).

    Parameters:
    ----------------------------------------------------------------
    jobID:     jobID of the job record
    fields:    list of fields to return

    Returns:    A sequence of field values in the same order as the requested
                 field list -> [field1, field2, ...]
    """
    # NOTE: jobsGetFields retries on transient mysql failures
    return self.jobsGetFields([jobID], fields, requireAll=True)[0][1]