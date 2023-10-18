def render(self, *args, **kwargs):
    '''
    Creates a <title> tag if not present and renders the DOCTYPE and tag tree.
    '''
    r = []

    #Validates the tag tree and adds the doctype if one was set
    if self.doctype:
      r.append(self.doctype)
      r.append('\n')
    r.append(super(document, self).render(*args, **kwargs))

    return u''.join(r)