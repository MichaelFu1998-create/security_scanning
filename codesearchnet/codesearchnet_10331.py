def setup(filename=CONFIGNAME):
     """Prepare a default GromacsWrapper global environment.

     1) Create the global config file.
     2) Create the directories in which the user can store template and config files.

     This function can be run repeatedly without harm.
     """
     # setup() must be separate and NOT run automatically when config
     # is loaded so that easy_install installations work
     # (otherwise we get a sandbox violation)
     # populate cfg with defaults (or existing data)
     get_configuration()
     if not os.path.exists(filename):
          with open(filename, 'w') as configfile:
               cfg.write(configfile)  # write the default file so that user can edit
               msg = "NOTE: GromacsWrapper created the configuration file \n\t%r\n" \
                     "      for you. Edit the file to customize the package." % filename
               print(msg)

     # directories
     for d in config_directories:
          utilities.mkdir_p(d)