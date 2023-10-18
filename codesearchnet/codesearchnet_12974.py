def _run_qmc(self, boot):
        """ runs quartet max-cut on a quartets file """

        ## convert to txt file for wQMC
        self._tmp = os.path.join(self.dirs, ".tmpwtre")
        cmd = [ip.bins.qmc, "qrtt="+self.files.qdump, "otre="+self._tmp] 

        ## run them
        proc = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        res = proc.communicate()
        if proc.returncode:
            #LOGGER.error("Error in QMC: \n({}).".format(res))
            LOGGER.error(res)
            raise IPyradWarningExit(res[1])

        ## read in the tmp files since qmc does not pipe
        with open(self._tmp) as intree:
            ## convert int names back to str names renamer returns a newick str
            #tmp = toytree.tree(intree.read().strip())
            tmp = ete3.Tree(intree.read().strip())
            tmpwtre = self._renamer(tmp)#.tree)

        ## save the tree
        if boot:
            self.trees.boots = os.path.join(self.dirs, self.name+".boots")
            with open(self.trees.boots, 'a') as outboot:
                outboot.write(tmpwtre+"\n")
        else:
            self.trees.tree = os.path.join(self.dirs, self.name+".tree")
            with open(self.trees.tree, 'w') as outtree:
                outtree.write(tmpwtre)

        ## save JSON file checkpoint
        self._save()