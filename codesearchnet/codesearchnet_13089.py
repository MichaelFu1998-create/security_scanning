def _load(self, name, workdir, quiet=False):
        """
        Load a JSON serialized tetrad instance to continue from a checkpoint.
        """

        ## load the JSON string and try with name+.json
        path = os.path.join(workdir, name)
        if not path.endswith(".tet.json"):
            path += ".tet.json"

        ## expand user
        path = path.replace("~", os.path.expanduser("~"))

        ## load the json file as a dictionary
        try:
            with open(path, 'r') as infile:
                fullj = _byteify(json.loads(infile.read(),
                                object_hook=_byteify), 
                            ignore_dicts=True)
        except IOError:
            raise IPyradWarningExit("""\
        Cannot find checkpoint (.tet.json) file at: {}""".format(path))

        ## set old attributes into new tetrad object
        self.name = fullj["name"]
        self.files.data = fullj["files"]["data"]
        self.files.mapfile = fullj["files"]["mapfile"]        
        self.dirs = fullj["dirs"]
        self._init_seqarray(quiet=quiet)
        self._parse_names()

        ## fill in the same attributes
        for key in fullj:
            ## fill Params a little different
            if key in ["files", "params", "database", 
                       "trees", "stats", "checkpoint"]:
                filler = fullj[key]
                for ikey in filler:
                    self.__dict__[key].__setattr__(ikey, fullj[key][ikey])
            else:
                self.__setattr__(key, fullj[key])