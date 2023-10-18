def modelsGetFieldsForCheckpointed(self, jobID, fields):
    """
    Gets fields from all models in a job that have been checkpointed. This is
    used to figure out whether or not a new model should be checkpointed.

    Parameters:
    -----------------------------------------------------------------------
    jobID:                    The jobID for the models to be searched
    fields:                   A list of fields to return

    Returns: a (possibly-empty) list of tuples as follows
      [
        (model_id1, [field1, ..., fieldn]),
        (model_id2, [field1, ..., fieldn]),
        (model_id3, [field1, ..., fieldn])
                    ...
      ]
    """

    assert len(fields) >= 1, "fields is empty"

    # Get a database connection and cursor
    with ConnectionFactory.get() as conn:
      dbFields = [self._models.pubToDBNameDict[f] for f in fields]
      dbFieldStr = ", ".join(dbFields)

      query = 'SELECT model_id, {fields} from {models}' \
              '   WHERE job_id=%s AND model_checkpoint_id IS NOT NULL'.format(
        fields=dbFieldStr, models=self.modelsTableName)

      conn.cursor.execute(query, [jobID])
      rows = conn.cursor.fetchall()

    return [(r[0], list(r[1:])) for r in rows]