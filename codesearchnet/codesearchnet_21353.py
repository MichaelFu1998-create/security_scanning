def append(self, listIndex, changeType, initialValue=None, isMd5=False):
    '''
    Adds a change spec to the current list of changes. The `listIndex`
    represents the line number (in multi-line mode) or word number (in
    single-line mode), and must be **INCLUSIVE** of both additions and
    deletions.
    '''
    if not isMd5 and initialValue is not None and len(initialValue) > 32:
      initialValue = hashlib.md5(initialValue).hexdigest()
      isMd5        = True
    cur = adict(index = int(listIndex),
                op    = changeType,
                ival  = initialValue,
                md5   = isMd5)
    for idx, val in enumerate(self.current):
      if val.index < cur.index:
        continue
      if val.index > cur.index:
        self.current.insert(idx, cur)
        break
      # todo: this should never happen... (there should not be a change
      #       reported for the same line without a `pushChangeSpec()` between)
      # todo: perhaps attempt a merging?...
      raise InvalidChangeSpec('conflicting changes for index %d' % (cur.index,))
    else:
      self.current.append(cur)