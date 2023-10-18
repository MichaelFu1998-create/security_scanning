def copy(self, new_object):
    """copy an object"""
    new_object.classdesc = self.classdesc

    for name in self.classdesc.fields_names:
      new_object.__setattr__(name, getattr(self, name))