def fetch_runinfo(self, fields=None, quiet=False):
        """
        Call esearch to grep SRR info for a project (SRP). Use the command
        sra.fetch_fields to see available fields to be fetched. This function
        returns a DataFrame with runinfo for the selected fields.

        Parameters:
        -----------
        Fields: (tuple or list)
            The default fields returned are 1-30. You can enter a list 
            or tuple of fewer numbers to select fewer fields. Example, 
            (1,4,6,29,30) returns a neat dataframe with Run IDs, 
            Number of reads (SE and PE), ScientificName, and SampleName. 
        """
        if not quiet:
            print("\rFetching project data...", end="")

        ## if no entry then fetch (nearly) all fields.
        if fields == None:  
            fields = range(30)
        fields = fields_checker(fields)

        ## command strings
        es_cmd = [
            "esearch", 
            "-db", "sra", 
            "-query", self.accession,
        ]

        ef_cmd = [
            "efetch", 
            "--format", "runinfo",
        ]

        cut_cmd = [
            "cut", 
            "-d", ",", 
            "-f", ",".join(fields),
        ]

        ## pipe commands together
        proc1 = sps.Popen(es_cmd, stderr=sps.STDOUT, stdout=sps.PIPE)
        proc2 = sps.Popen(ef_cmd, stdin=proc1.stdout, stderr=sps.STDOUT, stdout=sps.PIPE)
        proc3 = sps.Popen(cut_cmd, stdin=proc2.stdout, stderr=sps.STDOUT, stdout=sps.PIPE)
        o, e = proc3.communicate()
        proc2.stdout.close()
        proc1.stdout.close()
        
        if o:
            vals = o.strip().split("\n")
            names = vals[0].split(",")
            items = [i.split(",") for i in vals[1:] if i not in ["", vals[0]]]
            return pd.DataFrame(items, columns=names)
        else:
            raise IPyradWarningExit("no samples found in {}".format(self.accession))