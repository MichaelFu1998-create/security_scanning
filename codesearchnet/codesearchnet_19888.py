def tryLoadingFrom(tryPath,moduleName='swhlab'):
    """if the module is in this path, load it from the local folder."""
    if not 'site-packages' in swhlab.__file__:
        print("loaded custom swhlab module from",
              os.path.dirname(swhlab.__file__))
        return # no need to warn if it's already outside.
    while len(tryPath)>5:
        sp=tryPath+"/swhlab/" # imaginary swhlab module path
        if os.path.isdir(sp) and os.path.exists(sp+"/__init__.py"):
            if not os.path.dirname(tryPath) in sys.path:
                sys.path.insert(0,os.path.dirname(tryPath))
            print("#"*80)
            print("# WARNING: using site-packages swhlab module")
            print("#"*80)
        tryPath=os.path.dirname(tryPath)
    return