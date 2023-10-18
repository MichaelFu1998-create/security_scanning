def save_module(self, obj):
    """
    Save a module as an import
    """
    self.modules.add(obj)
    self.save_reduce(subimport, (obj.__name__,), obj=obj)