def run(self, steps=None, ipyclient=None, force=False, quiet=False):
        """
        Submits an ordered list of jobs to a load-balancer to complete 
        the following tasks, and reports a progress bar:
        (1) Write nexus files for each locus
        (2) Run mrBayes on each locus to get a posterior of gene trees
        (3) Run mbsum (a bucky tool) on the posterior set of trees
        (4) Run Bucky on the summarized set of trees for all alpha values.

        Parameters:
        -----------
        ipyclient (ipyparallel.Client())
            A connected ipyparallel Client object used to distribute jobs
        force (bool):
            Whether to overwrite existing files with the same name and workdir
            if they exist. Default is False.
        quiet (bool):
            Whether to suppress progress information. Default is False.
        steps (list):
            A list of integers of steps to perform. This is useful if a 
            job was interrupted, or you created a new bucky object copy, 
            or you wish to run an analysis under a new set of parameters, 
            after having run it once. For example, if you finished running
            steps 1 and 2 (write nexus files and infer mrbayes posteriors), 
            but you want to rerun steps 3 and 4 with new settings, then you
            could enter `steps=[3,4]` and also `force=True` to run steps 3 
            and 4 with a new set of parameters. Default argument is None 
            which means run all steps. 
        """

        ## require ipyclient
        if not ipyclient:
            raise IPyradWarningExit("an ipyclient object is required")

        ## check the steps argument
        if not steps:
            steps = [1, 2, 3, 4]
        if isinstance(steps, (int, str)):
            steps = [int(i) for i in [steps]]
        if isinstance(steps, list):
            if not all(isinstance(i, int) for i in steps):
                raise IPyradWarningExit("steps must be a list of integers")

        ## run steps ------------------------------------------------------
        ## TODO: wrap this function so it plays nice when interrupted.
        if 1 in steps:
            self.write_nexus_files(force=force, quiet=quiet)
        if 2 in steps:
            self.run_mrbayes(force=force, quiet=quiet, ipyclient=ipyclient)
        if 3 in steps:
            self.run_mbsum(force=force, quiet=quiet, ipyclient=ipyclient)
        if 4 in steps:
            self.run_bucky(force=force, quiet=quiet, ipyclient=ipyclient)

        ## make sure jobs are done if waiting (TODO: maybe make this optional)
        ipyclient.wait()