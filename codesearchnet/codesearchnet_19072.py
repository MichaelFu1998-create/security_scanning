def _loadNamelistIncludes(item, unique_glyphs, cache):
  """Load the includes of an encoding Namelist files.

  This is an implementation detail of readNamelist.
  """
  includes = item["includes"] = []
  charset = item["charset"] = set() | item["ownCharset"]

  noCharcode = item["noCharcode"] = set() | item["ownNoCharcode"]

  dirname =  os.path.dirname(item["fileName"])
  for include in item["header"]["includes"]:
    includeFile = os.path.join(dirname, include)
    try:
      includedItem = readNamelist(includeFile, unique_glyphs, cache)
    except NamelistRecursionError:
      continue
    if includedItem in includes:
      continue
    includes.append(includedItem)
    charset |= includedItem["charset"]
    noCharcode |= includedItem["ownNoCharcode"]
  return item