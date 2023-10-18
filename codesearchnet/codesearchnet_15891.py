def _cleanup(self):
        """Clean up resources used by the session.
        """
        self.exit()
        workspace = osp.join(os.getcwd(), 'octave-workspace')
        if osp.exists(workspace):
            os.remove(workspace)