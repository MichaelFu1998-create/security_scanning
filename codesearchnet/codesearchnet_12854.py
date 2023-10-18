def get_params(self, param=""):
        """ pretty prints params if called as a function """
        fullcurdir = os.path.realpath(os.path.curdir)
        if not param:
            for index, (key, value) in enumerate(self.paramsdict.items()):
                if isinstance(value, str):
                    value = value.replace(fullcurdir+"/", "./")
                sys.stdout.write("{}{:<4}{:<28}{:<45}\n"\
                    .format(self._spacer, index, key, value))
        else:
            try:
                if int(param):
                    #sys.stdout.write(self.paramsdict.values()[int(param)-1])
                    return self.paramsdict.values()[int(param)]
            except (ValueError, TypeError, NameError, IndexError):
                try:
                    return self.paramsdict[param]
                except KeyError:
                    return 'key not recognized'