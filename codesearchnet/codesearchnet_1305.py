def modelsClearAll(self):
    """ Delete all models from the models table

    Parameters:
    ----------------------------------------------------------------
    """
    self._logger.info('Deleting all rows from models table %r',
                      self.modelsTableName)
    with ConnectionFactory.get() as conn:
      query = 'DELETE FROM %s' % (self.modelsTableName)
      conn.cursor.execute(query)