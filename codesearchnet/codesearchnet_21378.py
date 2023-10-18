def cmpToDataStore_uri(base, ds1, ds2):
  '''Bases the comparison of the datastores on URI alone.'''
  ret = difflib.get_close_matches(base.uri, [ds1.uri, ds2.uri], 1, cutoff=0.5)
  if len(ret) <= 0:
    return 0
  if ret[0] == ds1.uri:
    return -1
  return 1