def _check_version():
    """ Test if there's a newer version and nag the user to upgrade."""
    import urllib2
    from distutils.version import LooseVersion

    header = \
    "\n -------------------------------------------------------------"+\
    "\n  ipyrad [v.{}]".format(ip.__version__)+\
    "\n  Interactive assembly and analysis of RAD-seq data"+\
    "\n -------------------------------------------------------------"

    try:
        htmldat = urllib2.urlopen("https://anaconda.org/ipyrad/ipyrad").readlines()
        curversion = next((x for x in htmldat if "subheader" in x), None).split(">")[1].split("<")[0]
        if LooseVersion(ip.__version__) < LooseVersion(curversion):
            msg = """
  A new version of ipyrad is available (v.{}). To upgrade run:

    conda install -c ipyrad ipyrad\n""".format(curversion)
            print(header + "\n" + msg)
        else:
            pass
            #print("You are up to date")
    except Exception as inst:
        ## Always fail silently
        pass