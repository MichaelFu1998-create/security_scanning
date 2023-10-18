def __readNamelist(cache, filename, unique_glyphs):
  """Return a dict with the data of an encoding Namelist file.

  This is an implementation detail of readNamelist.
  """
  if filename in cache:
    item = cache[filename]
  else:
    cps, header, noncodes = parseNamelist(filename)
    item = {
      "fileName": filename
    , "ownCharset": cps
    , "header": header
    , "ownNoCharcode": noncodes
    , "includes": None # placeholder
    , "charset": None # placeholder
    , "noCharcode": None
    }
    cache[filename] = item

  if unique_glyphs or item["charset"] is not None:
    return item

  # full-charset/includes are requested and not cached yet
  _loadNamelistIncludes(item, unique_glyphs, cache)
  return item