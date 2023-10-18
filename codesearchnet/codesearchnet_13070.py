def _getbins():
    """ gets the right version of vsearch, muscle, and smalt
    depending on linux vs osx """

    # Return error if system is 32-bit arch.
    # This is straight from the python docs:
    # https://docs.python.org/2/library/platform.html#cross-platform
    if not _sys.maxsize > 2**32:
        _sys.exit("ipyrad requires 64bit architecture")

    ## get platform mac or linux
    _platform = _sys.platform

    ## get current location
    if 'VIRTUAL_ENV' in _os.environ:
        ipyrad_path = _os.environ['VIRTUAL_ENV']
    else:
        path = _os.path.abspath(_os.path.dirname(__file__))
        ipyrad_path = _os.path.dirname(path)

    ## find bin directory
    ipyrad_path = _os.path.dirname(path)
    bin_path = _os.path.join(ipyrad_path, "bin")

    ## get the correct binaries
    if 'linux' in _platform:
        vsearch = _os.path.join(
                       _os.path.abspath(bin_path),
                       "vsearch-linux-x86_64")
        muscle = _os.path.join(
                       _os.path.abspath(bin_path),
                       "muscle-linux-x86_64")
        smalt = _os.path.join(
                       _os.path.abspath(bin_path),
                       "smalt-linux-x86_64")
        bwa = _os.path.join(
                       _os.path.abspath(bin_path),
                       "bwa-linux-x86_64")
        samtools = _os.path.join(
                       _os.path.abspath(bin_path),
                       "samtools-linux-x86_64")
        bedtools = _os.path.join(
                       _os.path.abspath(bin_path),
                       "bedtools-linux-x86_64")
        qmc = _os.path.join(
                       _os.path.abspath(bin_path),
                       "QMC-linux-x86_64")
    else:
        vsearch = _os.path.join(
                       _os.path.abspath(bin_path),
                       "vsearch-osx-x86_64")
        muscle = _os.path.join(
                       _os.path.abspath(bin_path),
                       "muscle-osx-x86_64")
        smalt = _os.path.join(
                       _os.path.abspath(bin_path),
                       "smalt-osx-x86_64")
        bwa = _os.path.join(
                       _os.path.abspath(bin_path),
                       "bwa-osx-x86_64")
        samtools = _os.path.join(
                       _os.path.abspath(bin_path),
                       "samtools-osx-x86_64")
        bedtools = _os.path.join(
                       _os.path.abspath(bin_path),
                       "bedtools-osx-x86_64")
        ## only one compiled version available, works for all?
        qmc = _os.path.join(
                       _os.path.abspath(bin_path),
                       "QMC-osx-x86_64")

    # Test for existence of binaries
    assert _cmd_exists(muscle), "muscle not found here: "+muscle
    assert _cmd_exists(vsearch), "vsearch not found here: "+vsearch
    assert _cmd_exists(smalt), "smalt not found here: "+smalt
    assert _cmd_exists(bwa), "bwa not found here: "+bwa
    assert _cmd_exists(samtools), "samtools not found here: "+samtools
    assert _cmd_exists(bedtools), "bedtools not found here: "+bedtools
    #assert _cmd_exists(qmc), "wQMC not found here: "+qmc
    return vsearch, muscle, smalt, bwa, samtools, bedtools, qmc