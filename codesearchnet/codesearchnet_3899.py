def import_module_from_path(modpath, index=-1):
    """
    Imports a module via its path

    Args:
        modpath (PathLike): path to the module on disk or within a zipfile.

    Returns:
        module: the imported module

    References:
        https://stackoverflow.com/questions/67631/import-module-given-path

    Notes:
        If the module is part of a package, the package will be imported first.
        These modules may cause problems when reloading via IPython magic

        This can import a module from within a zipfile. To do this modpath
        should specify the path to the zipfile and the path to the module
        within that zipfile separated by a colon or pathsep.
        E.g. `/path/to/archive.zip:mymodule.py`

    Warning:
        It is best to use this with paths that will not conflict with
        previously existing modules.

        If the modpath conflicts with a previously existing module name. And
        the target module does imports of its own relative to this conflicting
        path. In this case, the module that was loaded first will win.

        For example if you try to import '/foo/bar/pkg/mod.py' from the folder
        structure:
          - foo/
            +- bar/
               +- pkg/
                  +  __init__.py
                  |- mod.py
                  |- helper.py

       If there exists another module named `pkg` already in sys.modules
       and mod.py does something like `from . import helper`, Python will
       assume helper belongs to the `pkg` module already in sys.modules.
       This can cause a NameError or worse --- a incorrect helper module.

    Example:
        >>> import xdoctest
        >>> modpath = xdoctest.__file__
        >>> module = import_module_from_path(modpath)
        >>> assert module is xdoctest

    Example:
        >>> # Test importing a module from within a zipfile
        >>> import zipfile
        >>> from xdoctest import utils
        >>> from os.path import join, expanduser
        >>> dpath = expanduser('~/.cache/xdoctest')
        >>> dpath = utils.ensuredir(dpath)
        >>> #dpath = utils.TempDir().ensure()
        >>> # Write to an external module named bar
        >>> external_modpath = join(dpath, 'bar.py')
        >>> open(external_modpath, 'w').write('testvar = 1')
        >>> internal = 'folder/bar.py'
        >>> # Move the external bar module into a zipfile
        >>> zippath = join(dpath, 'myzip.zip')
        >>> with zipfile.ZipFile(zippath, 'w') as myzip:
        >>>     myzip.write(external_modpath, internal)
        >>> # Import the bar module from within the zipfile
        >>> modpath = zippath + ':' + internal
        >>> modpath = zippath + os.path.sep + internal
        >>> module = import_module_from_path(modpath)
        >>> assert module.__name__ == os.path.normpath('folder/bar')
        >>> assert module.testvar == 1

    Doctest:
        >>> import pytest
        >>> with pytest.raises(IOError):
        >>>     import_module_from_path('does-not-exist')
        >>> with pytest.raises(IOError):
        >>>     import_module_from_path('does-not-exist.zip/')
    """
    import os
    if not os.path.exists(modpath):
        import re
        import zipimport
        # We allow (if not prefer or force) the colon to be a path.sep in order
        # to agree with the mod.__name__ attribute that will be produced

        # zip followed by colon or slash
        pat = '(.zip[' + re.escape(os.path.sep) + '/:])'
        parts = re.split(pat, modpath, flags=re.IGNORECASE)
        if len(parts) > 2:
            archivepath = ''.join(parts[:-1])[:-1]
            internal = parts[-1]
            modname = os.path.splitext(internal)[0]
            modname = os.path.normpath(modname)
            if os.path.exists(archivepath):
                zimp_file = zipimport.zipimporter(archivepath)
                module = zimp_file.load_module(modname)
                return module
        raise IOError('modpath={} does not exist'.format(modpath))
    else:
        # the importlib version doesnt work in pytest
        module = _custom_import_modpath(modpath)
        # TODO: use this implementation once pytest fixes importlib
        # module = _pkgutil_import_modpath(modpath)
        return module