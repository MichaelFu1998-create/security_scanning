def check_setup():
     """Check if templates directories are setup and issue a warning and help.

    Set the environment variable  :envvar:`GROMACSWRAPPER_SUPPRESS_SETUP_CHECK`
    skip the check and make it always return ``True``

    :return ``True`` if directories were found and ``False`` otherwise

     .. versionchanged:: 0.3.1
        Uses :envvar:`GROMACSWRAPPER_SUPPRESS_SETUP_CHECK` to suppress check
        (useful for scripts run on a server)
     """

     if "GROMACSWRAPPER_SUPPRESS_SETUP_CHECK" in os.environ:
         return True

     missing = [d for d in config_directories if not os.path.exists(d)]
     if len(missing) > 0:
         print("NOTE: Some configuration directories are not set up yet: ")
         print("\t{0!s}".format('\n\t'.join(missing)))
         print("NOTE: You can create the configuration file and directories with:")
         print("\t>>> import gromacs")
         print("\t>>> gromacs.config.setup()")
         return False
     return True