def copy(self, name, load_existing_results=False):
        """ 
        Returns a copy of the bpp object with the same parameter settings
        but with the files.mcmcfiles and files.outfiles attributes cleared, 
        and with a new 'name' attribute. 
        
        Parameters
        ----------
        name (str):
            A name for the new copied bpp object that will be used for the 
            output files created by the object. 

        """

        ## make deepcopy of self.__dict__ but do not copy async objects
        subdict = {i:j for i,j in self.__dict__.iteritems() if i != "asyncs"}
        newdict = copy.deepcopy(subdict)

        ## make back into a bpp object
        if name == self.name:
            raise Exception("new object must have a different 'name' than its parent")
        newobj = Bpp(
            name=name,
            data=newdict["files"].data,
            workdir=newdict["workdir"],
            guidetree=newdict["tree"].write(),
            imap={i:j for i, j in newdict["imap"].items()},
            copied=True,
            load_existing_results=load_existing_results,
            )

        ## update special dict attributes but not files
        for key, val in newobj.params.__dict__.iteritems():
            newobj.params.__setattr__(key, self.params.__getattribute__(key))
        for key, val in newobj.filters.__dict__.iteritems():
            newobj.filters.__setattr__(key, self.filters.__getattribute__(key))

        ## new object must have a different name than it's parent
        return newobj