def configuration(self):
          """Dict of variables that we make available as globals in the module.

          Can be used as ::

             globals().update(GMXConfigParser.configuration)        # update configdir, templatesdir ...
          """
          configuration = {
               'configfilename': self.filename,
               'logfilename': self.getpath('Logging', 'logfilename'),
               'loglevel_console': self.getLogLevel('Logging', 'loglevel_console'),
               'loglevel_file': self.getLogLevel('Logging', 'loglevel_file'),
               'configdir': self.getpath('DEFAULT', 'configdir'),
               'qscriptdir': self.getpath('DEFAULT', 'qscriptdir'),
               'templatesdir': self.getpath('DEFAULT', 'templatesdir'),
               }
          configuration['path'] = [os.path.curdir,
                                   configuration['qscriptdir'],
                                   configuration['templatesdir']]
          return configuration