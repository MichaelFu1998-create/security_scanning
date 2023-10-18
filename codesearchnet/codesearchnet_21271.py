def configure(self, argv=None):
    '''
    Configures this engine based on the options array passed into
    `argv`. If `argv` is ``None``, then ``sys.argv`` is used instead.
    During configuration, the command line options are merged with
    previously stored values. Then the logging subsystem and the
    database model are initialized, and all storable settings are
    serialized to configurations files.
    '''
    self._setupOptions()
    self._parseOptions(argv)
    self._setupLogging()
    self._setupModel()
    self.dbsession.commit()
    return self