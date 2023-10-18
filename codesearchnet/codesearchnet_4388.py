def attr(*args, **kwargs):
  '''
  Set attributes on the current active tag context
  '''
  ctx = dom_tag._with_contexts[_get_thread_context()]
  if ctx and ctx[-1]:
    dicts = args + (kwargs,)
    for d in dicts:
      for attr, value in d.items():
        ctx[-1].tag.set_attribute(*dom_tag.clean_pair(attr, value))
  else:
    raise ValueError('not in a tag context')