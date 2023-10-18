def branch(self, newname, subsamples=None, infile=None):
        """
        Returns a copy of the Assembly object. Does not allow Assembly
        object names to be replicated in namespace or path.
        """
        ## subsample by removal or keeping.
        remove = 0

        ## is there a better way to ask if it already exists?
        if (newname == self.name or os.path.exists(
                                    os.path.join(self.paramsdict["project_dir"],
                                    newname+".assembly"))):
            print("{}Assembly object named {} already exists"\
                  .format(self._spacer, newname))

        else:
            ## Make sure the new name doesn't have any wacky characters
            self._check_name(newname)

            ## Bozo-check. Carve off 'params-' if it's in the new name.
            if newname.startswith("params-"):
                newname = newname.split("params-")[1]

            ## create a copy of the Assembly obj
            newobj = copy.deepcopy(self)
            newobj.name = newname
            newobj.paramsdict["assembly_name"] = newname

            if subsamples and infile:
                print(BRANCH_NAMES_AND_INPUT)

            if infile:
                if infile[0] == "-":
                    remove = 1
                    infile = infile[1:]
                if os.path.exists(infile):
                    subsamples = _read_sample_names(infile)

            ## if remove then swap the samples
            if remove:
                subsamples = list(set(self.samples.keys()) - set(subsamples))

            ## create copies of each subsampled Sample obj
            if subsamples:
                for sname in subsamples:
                    if sname in self.samples:
                        newobj.samples[sname] = copy.deepcopy(self.samples[sname])
                    else:
                        print("Sample name not found: {}".format(sname))

                ## reload sample dict w/o non subsamples
                newobj.samples = {name:sample for name, sample in \
                           newobj.samples.items() if name in subsamples}

            ## create copies of each subsampled Sample obj
            else:
                for sample in self.samples:
                    newobj.samples[sample] = copy.deepcopy(self.samples[sample])

            ## save json of new obj and return object
            newobj.save()
            return newobj