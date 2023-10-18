def save_function(self, obj, name=None):
    """ Registered with the dispatch to handle all function types.
    Determines what kind of function obj is (e.g. lambda, defined at
    interactive prompt, etc) and handles the pickling appropriately.
    """
    write = self.write

    if name is None:
      name = obj.__name__
    try:
      # whichmodule() could fail, see
      # https://bitbucket.org/gutworth/six/issues/63/importing-six-breaks-pickling
      modname = pickle.whichmodule(obj, name)
    except Exception:
      modname = None
    # print('which gives %s %s %s' % (modname, obj, name))
    try:
      themodule = sys.modules[modname]
    except KeyError:
      # eval'd items such as namedtuple give invalid items for their function __module__
      modname = '__main__'

    if modname == '__main__':
      themodule = None

    if themodule:
      self.modules.add(themodule)
      if getattr(themodule, name, None) is obj:
        return self.save_global(obj, name)

    # if func is lambda, def'ed at prompt, is in main, or is nested, then
    # we'll pickle the actual function object rather than simply saving a
    # reference (as is done in default pickler), via save_function_tuple.
    if islambda(obj) or obj.__code__.co_filename == '<stdin>' or themodule is None:
      #print("save global", islambda(obj), obj.__code__.co_filename, modname, themodule)
      self.save_function_tuple(obj)
      return
    else:
      # func is nested
      klass = getattr(themodule, name, None)
      if klass is None or klass is not obj:
        self.save_function_tuple(obj)
        return

    if obj.__dict__:
      # essentially save_reduce, but workaround needed to avoid recursion
      self.save(_restore_attr)
      write(pickle.MARK + pickle.GLOBAL + modname + '\n' + name + '\n')
      self.memoize(obj)
      self.save(obj.__dict__)
      write(pickle.TUPLE + pickle.REDUCE)
    else:
      write(pickle.GLOBAL + modname + '\n' + name + '\n')
      self.memoize(obj)