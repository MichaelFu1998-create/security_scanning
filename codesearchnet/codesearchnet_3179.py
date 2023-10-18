def visualize(self):
        """
        Given a Manticore workspace, or trace file, highlight the basic blocks.
        """
        if os.path.isfile(self.workspace):
            t = threading.Thread(target=self.highlight_from_file,
                                 args=(self.workspace,))
        elif os.path.isdir(self.workspace):
            t = threading.Thread(target=self.highlight_from_dir,
                                 args=(self.workspace,))
        t.start()