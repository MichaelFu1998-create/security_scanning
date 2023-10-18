def dictDiffAndReport(da, db):
  """ Compares two python dictionaries at the top level and report differences,
  if any, to stdout

  da:             first dictionary
  db:             second dictionary

  Returns:        The same value as returned by dictDiff() for the given args
  """
  differences = dictDiff(da, db)

  if not differences:
    return differences

  if differences['inAButNotInB']:
    print ">>> inAButNotInB: %s" % differences['inAButNotInB']

  if differences['inBButNotInA']:
    print ">>> inBButNotInA: %s" % differences['inBButNotInA']

  for key in differences['differentValues']:
    print ">>> da[%s] != db[%s]" % (key, key)
    print "da[%s] = %r" % (key, da[key])
    print "db[%s] = %r" % (key, db[key])

  return differences