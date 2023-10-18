def _check_extmodule(module, formatkey):
    '''This imports the module specified.

    Used to dynamically import Python modules that are needed to support LC
    formats not natively supported by astrobase.

    Parameters
    ----------

    module : str
        This is either:

        - a Python module import path, e.g. 'astrobase.lcproc.catalogs' or
        - a path to a Python file, e.g. '/astrobase/hatsurveys/hatlc.py'

        that contains the Python module that contains functions used to open
        (and optionally normalize) a custom LC format that's not natively
        supported by astrobase.

    formatkey : str
        A str used as the unique ID of this LC format for all lcproc functions
        and can be used to look it up later and import the correct functions
        needed to support it for lcproc operations. For example, we use
        'kep-fits' as a the specifier for Kepler FITS light curves, which can be
        read by the `astrobase.astrokep.read_kepler_fitslc` function as
        specified by the `<astrobase install path>/data/lcformats/kep-fits.json`
        LC format specification JSON.

    Returns
    -------

    Python module
        This returns a Python module if it's able to successfully import it.

    '''

    try:

        if os.path.exists(module):

            sys.path.append(os.path.dirname(module))
            importedok = importlib.import_module(
                os.path.basename(module.replace('.py',''))
            )

        else:
            importedok = importlib.import_module(module)

    except Exception as e:

        LOGEXCEPTION('could not import the module: %s for LC format: %s. '
                     'check the file path or fully qualified module name?'
                     % (module, formatkey))
        importedok = False

    return importedok