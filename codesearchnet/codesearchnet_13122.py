def run(self, 
        ipyclient=None, 
        quiet=False,
        force=False,
        block=False,
        ):
        """
        Submits raxml job to run. If no ipyclient object is provided then 
        the function will block until the raxml run is finished. If an ipyclient
        is provided then the job is sent to a remote engine and an asynchronous 
        result object is returned which can be queried or awaited until it finishes.

        Parameters
        -----------
        ipyclient:
            Not yet supported... 
        quiet: 
            suppress print statements
        force:
            overwrite existing results files with this job name. 
        block:
            will block progress in notebook until job finishes, even if job
            is running on a remote ipyclient.
        """

        ## stop before trying in raxml
        if force:
            for key, oldfile in self.trees:
                if os.path.exists(oldfile):
                    os.remove(oldfile)
        if os.path.exists(self.trees.info):
            print("Error: set a new name for this job or use Force flag.\nFile exists: {}"\
                  .format(self.trees.info))
            return 

        ## TODO: add a progress bar tracker here. It could even read it from
        ## the info file that is being written. 
        ## submit it
        if not ipyclient:
            proc = _call_raxml(self._command_list)
            self.stdout = proc[0]
            self.stderr = proc[1]
        else:
            ## find all hosts and submit job to the host with most available engines
            lbview = ipyclient.load_balanced_view()
            self.async = lbview.apply(_call_raxml, self._command_list)

        ## initiate random seed
        if not quiet:
            if not ipyclient:
                ## look for errors
                if "Overall execution time" not in self.stdout:
                    print("Error in raxml run\n" + self.stdout)
                else:
                    print("job {} finished successfully".format(self.params.n))
            else:
                print("job {} submitted to cluster".format(self.params.n))