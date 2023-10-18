def read(self, filenames):
        '''' Read a list of files. Their configuration values are merged, with
             preference to values from files earlier in the list.
        '''
        for fn in filenames:
            try:
                self.configs[fn] = ordered_json.load(fn)
            except IOError:
                self.configs[fn] = OrderedDict()
            except Exception as e:
                self.configs[fn] = OrderedDict()
                logging.warning(
                    "Failed to read settings file %s, it will be ignored. The error was: %s",
                    fn, e
                )