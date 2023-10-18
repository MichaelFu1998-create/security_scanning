def setdocument(self, doc):
    '''
    Creates a reference to the parent document to allow for partial-tree
    validation.
    '''
    # assume that a document is correct in the subtree
    if self.document != doc:
      self.document = doc
      for i in self.children:
        if not isinstance(i, dom_tag): return
        i.setdocument(doc)