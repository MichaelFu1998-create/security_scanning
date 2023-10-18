def _pre_install():
    '''Initialize the parse table at install time'''

    # Generate the parsetab.dat file at setup time
    dat = join(setup_dir, 'src', 'hcl', 'parsetab.dat')
    if exists(dat):
        os.unlink(dat)

    sys.path.insert(0, join(setup_dir, 'src'))

    import hcl
    from hcl.parser import HclParser

    parser = HclParser()