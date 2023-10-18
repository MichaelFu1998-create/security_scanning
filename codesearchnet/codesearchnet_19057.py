def detect(text):
  """Detect the input's transliteration scheme.

    :param text: some text data, either a `unicode` or a `str` encoded
                 in UTF-8.
    """
  if sys.version_info < (3, 0):
    # Verify encoding
    try:
      text = text.decode('utf-8')
    except UnicodeError:
      pass

  # Brahmic schemes are all within a specific range of code points.
  for L in text:
    code = ord(L)
    if code >= BRAHMIC_FIRST_CODE_POINT:
      for name, start_code in BLOCKS:
        if start_code <= code <= BRAHMIC_LAST_CODE_POINT:
          return name

  # Romanizations
  if Regex.IAST_OR_KOLKATA_ONLY.search(text):
    if Regex.KOLKATA_ONLY.search(text):
      return Scheme.Kolkata
    else:
      return Scheme.IAST

  if Regex.ITRANS_ONLY.search(text):
    return Scheme.ITRANS

  if Regex.SLP1_ONLY.search(text):
    return Scheme.SLP1

  if Regex.VELTHUIS_ONLY.search(text):
    return Scheme.Velthuis

  if Regex.ITRANS_OR_VELTHUIS_ONLY.search(text):
    return Scheme.ITRANS

  return Scheme.HK