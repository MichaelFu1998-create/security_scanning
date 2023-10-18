def _run_qmc(self, boot):
        """
        Runs quartet max-cut QMC on the quartets qdump file.
        """

        ## build command
        self._tmp = os.path.join(self.dirs, ".tmptre")
        cmd = [ip.bins.qmc, "qrtt="+self.files.qdump, "otre="+self._tmp]

        ## run it
        proc = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        res = proc.communicate()
        if proc.returncode:
            raise IPyradWarningExit(res[1])

        ## parse tmp file written by qmc into a tree and rename it
        with open(self._tmp, 'r') as intree:
            tre = ete3.Tree(intree.read().strip())
            names = tre.get_leaves()
            for name in names:
                name.name = self.samples[int(name.name)]
            tmptre = tre.write(format=9)

        ## save the tree to file
        if boot:
            self.trees.boots = os.path.join(self.dirs, self.name+".boots")
            with open(self.trees.boots, 'a') as outboot:
                outboot.write(tmptre+"\n")
        else:
            self.trees.tree = os.path.join(self.dirs, self.name+".tree")
            with open(self.trees.tree, 'w') as outtree:
                outtree.write(tmptre)

        ## save the file
        self._save()