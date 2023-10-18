def copy(self, name):
        """ 
        Returns a copy of the treemix object with the same parameter settings
        but with the files attributes cleared, and with a new 'name' attribute. 
        
        Parameters
        ----------
        name (str):
            A name for the new copied treemix bject that will be used for the 
            output files created by the object. 

        """

        ## make deepcopy of self.__dict__ but do not copy async objects
        subdict = {i:j for i, j in self.__dict__.iteritems() if i != "asyncs"}
        newdict = copy.deepcopy(subdict)

        ## make back into a Treemix object
        #if name == self.name:
        #    raise Exception("new object name must be different from its parent")

        newobj = Treemix(
            data=newdict["data"],
            name=name,
            workdir=newdict["workdir"],
            imap={i:j for i, j in newdict["imap"].items()},
            mapfile=newdict['mapfile'],
            minmap={i:j for i, j in newdict["minmap"].items()},
            seed=np.random.randint(0, int(1e9)),
            )

        ## update special dict attributes but not files
        for key, val in newobj.params.__dict__.iteritems():
            newobj.params.__setattr__(key, self.params.__getattribute__(key))
        #for key, val in newobj.filters.__dict__.iteritems():
        #    newobj.filters.__setattr__(key, self.filters.__getattribute__(key))

        ## new object must have a different name than it's parent
        return newobj