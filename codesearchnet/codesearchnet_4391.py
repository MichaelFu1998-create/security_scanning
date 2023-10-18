def add(self, *args):
    '''
    Add new child tags.
    '''
    for obj in args:
      if isinstance(obj, numbers.Number):
        # Convert to string so we fall into next if block
        obj = str(obj)

      if isinstance(obj, basestring):
        obj = escape(obj)
        self.children.append(obj)

      elif isinstance(obj, dom_tag):
        ctx = dom_tag._with_contexts[_get_thread_context()]
        if ctx and ctx[-1]:
          ctx[-1].used.add(obj)
        self.children.append(obj)
        obj.parent = self
        obj.setdocument(self.document)

      elif isinstance(obj, dict):
        for attr, value in obj.items():
          self.set_attribute(*dom_tag.clean_pair(attr, value))

      elif hasattr(obj, '__iter__'):
        for subobj in obj:
          self.add(subobj)

      else:  # wtf is it?
        raise ValueError('%r not a tag or string.' % obj)

    if len(args) == 1:
      return args[0]

    return args