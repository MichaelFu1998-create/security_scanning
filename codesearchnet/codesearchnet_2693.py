def save_function_tuple(self, func):
    """  Pickles an actual func object.
    A func comprises: code, globals, defaults, closure, and dict.  We
    extract and save these, injecting reducing functions at certain points
    to recreate the func object.  Keep in mind that some of these pieces
    can contain a ref to the func itself.  Thus, a naive save on these
    pieces could trigger an infinite loop of save's.  To get around that,
    we first create a skeleton func object using just the code (this is
    safe, since this won't contain a ref to the func), and memoize it as
    soon as it's created.  The other stuff can then be filled in later.
    """
    save = self.save
    write = self.write

    code, f_globals, defaults, closure, dct, base_globals = self.extract_func_data(func)

    save(_fill_function)  # skeleton function updater
    write(pickle.MARK)    # beginning of tuple that _fill_function expects

    # create a skeleton function object and memoize it
    save(_make_skel_func)
    save((code, closure, base_globals))
    write(pickle.REDUCE)
    self.memoize(func)

    # save the rest of the func data needed by _fill_function
    save(f_globals)
    save(defaults)
    save(dct)
    save(func.__module__)
    write(pickle.TUPLE)
    write(pickle.REDUCE)