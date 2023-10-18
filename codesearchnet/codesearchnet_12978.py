def _save(self):
        """ save a JSON file representation of Tetrad Class for checkpoint"""

        ## save each attribute as dict
        fulldict = copy.deepcopy(self.__dict__)
        for i, j in fulldict.items():
            if isinstance(j, Params):
                fulldict[i] = j.__dict__
        fulldumps = json.dumps(fulldict,
                               sort_keys=False, 
                               indent=4, 
                               separators=(",", ":"),
                               )

        ## save to file, make dir if it wasn't made earlier
        assemblypath = os.path.join(self.dirs, self.name+".tet.json")
        if not os.path.exists(self.dirs):
            os.mkdir(self.dirs)
    
        ## protect save from interruption
        done = 0
        while not done:
            try:
                with open(assemblypath, 'w') as jout:
                    jout.write(fulldumps)
                done = 1
            except (KeyboardInterrupt, SystemExit): 
                print('.')
                continue