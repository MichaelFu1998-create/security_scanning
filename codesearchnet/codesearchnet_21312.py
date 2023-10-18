def scan(self, store):
    '''
    Scans the local files for changes (either additions, modifications or
    deletions) and reports them to the `store` object, which is expected to
    implement the :class:`pysyncml.Store` interface.
    '''
    # steps:
    #   1) generate a table of all store files, with filename,
    #      inode, checksum
    #   2) generate a table of all current files, with filename,
    #      inode, checksum
    #   3) iterate over all stored values and find matches, delete
    #      them from the "not-matched-yet" table, and record the
    #      change

    # TODO: if this engine is running as the client, i think the best
    #       strategy is to delete all pending changes before starting
    #       the scan process. that way, any left-over gunk from a
    #       previous sync that did not terminate well is cleaned up...

    # TODO: this algorithm, although better than the last, has the
    #       inconvenient downside of being very memory-hungry: it
    #       assumes that the entire list of notes (with sha256
    #       checksums - not the entire body) fits in memory. although
    #       it is not a ridiculous assumption (these are "notes" after
    #       all...), it would be nice if it did not rely on that.

    # todo: by tracking inode's, this *could* also potentially reduce
    #       some "del/add" operations with a single "mod"

    # todo: should this make use of lastmod timestamps?... that may
    #       help to reduce the number of checksums calculated and the
    #       number of entries loaded into memory...

    if self.ignoreRoot is None:
      self.ignoreRoot = re.compile('^(%s)$' % (re.escape(self.engine.syncSubdir),))

    dbnotes = list(self.engine.model.NoteItem.q())
    dbnames = dict((e.name, e) for e in dbnotes)

    fsnotes = list(self._scandir('.'))
    fsnames = dict((e.name, e) for e in fsnotes)

    # first pass: eliminate all entries with matching filenames & checksum

    for fsent in fsnames.values():
      if fsent.name in dbnames and dbnames[fsent.name].sha256 == fsent.sha256:
        log.debug('entry "%s" not modified', fsent.name)
        # todo: update db inode and lastmod if needed...
        del dbnames[fsent.name]
        del fsnames[fsent.name]

    # second pass: find entries that were moved to override another entry

    dbskip = []
    for dbent in dbnames.values():
      if dbent.id in dbskip or dbent.name in fsnames:
        continue
      for fsent in fsnames.values():
        if fsent.sha256 != dbent.sha256 or fsent.name not in dbnames:
          continue
        log.debug('entry "%s" deleted and replaced by "%s"', fsent.name, dbent.name)
        dbother = dbnames[fsent.name]
        del dbnames[dbent.name]
        del dbnames[fsent.name]
        del fsnames[fsent.name]
        dbskip.append(dbother.id)
        store.registerChange(dbent.id, pysyncml.ITEM_DELETED)
        for key, val in fsent.items():
          setattr(dbother, key, val)
        # the digest didn't change, so this is just a filename change...
        if self.engine.options.syncFilename:
          store.registerChange(dbother.id, pysyncml.ITEM_MODIFIED)
        break

    # third pass: find entries that were renamed

    dbskip = []
    for dbent in dbnames.values():
      if dbent.id in dbskip:
        continue
      for fsent in fsnames.values():
        if fsent.sha256 != dbent.sha256:
          continue
        log.debug('entry "%s" renamed to "%s"', dbent.name, fsent.name)
        del dbnames[dbent.name]
        del fsnames[fsent.name]
        for key, val in fsent.items():
          setattr(dbent, key, val)
        # the digest didn't change, so this is just a filename change...
        if self.engine.options.syncFilename:
          store.registerChange(dbent.id, pysyncml.ITEM_MODIFIED)
        break

    # fourth pass: find new and modified entries

    for fsent in fsnames.values():
      if fsent.name in dbnames:
        log.debug('entry "%s" modified', fsent.name)
        dbent = dbnames[fsent.name]
        del dbnames[fsent.name]
        store.registerChange(dbent.id, pysyncml.ITEM_MODIFIED)
      else:
        log.debug('entry "%s" added', fsent.name)
        dbent = self.engine.model.NoteItem()
        self.engine.dbsession.add(dbent)
        store.registerChange(dbent.id, pysyncml.ITEM_ADDED)
      for key, val in fsent.items():
        setattr(dbent, key, val)
      del fsnames[fsent.name]

    # fifth pass: find deleted entries

    for dbent in dbnames.values():
      store.registerChange(dbent.id, pysyncml.ITEM_DELETED)
      self.engine.dbsession.add(dbent)