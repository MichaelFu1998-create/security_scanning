def run_tree_inference(self, nexus, idx):
        """
        Write nexus to tmpfile, runs phyml tree inference, and parses
        and returns the resulting tree. 
        """
        ## create a tmpdir for this test
        tmpdir = tempfile.tempdir
        tmpfile = os.path.join(tempfile.NamedTemporaryFile(
            delete=False,
            prefix=str(idx),
            dir=tmpdir,
        ))

        ## write nexus to tmpfile
        tmpfile.write(nexus)
        tmpfile.flush()

        ## infer the tree
        rax = raxml(name=str(idx), data=tmpfile.name, workdir=tmpdir, N=1, T=2)
        rax.run(force=True, block=True, quiet=True)

        ## clean up
        tmpfile.close()

        ## return tree order
        order = get_order(toytree.tree(rax.trees.bestTree))
        return "".join(order)