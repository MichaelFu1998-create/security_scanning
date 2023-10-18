def open(self):
        """open the drop box

        You need to call this method before starting putting packages.

        Returns
        -------
        None

        """

        self.workingArea.open()
        self.runid_pkgidx_map = { }
        self.runid_to_return = deque()