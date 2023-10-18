def stitch(self, folder=None):
        """Stitches all wells in experiment with ImageJ. Stitched images are
        saved in experiment root.

        Images which already exists are omitted stitching.

        Parameters
        ----------
        folder : string
            Where to store stitched images. Defaults to experiment path.

        Returns
        -------
        list
            Filenames of stitched images. Files which already exists before
            stitching are also returned.
        """
        debug('stitching ' + self.__str__())
        if not folder:
            folder = self.path

        # create list of macros and files
        macros = []
        files = []
        for well in self.wells:
            f,m = stitch_macro(well, folder)
            macros.extend(m)
            files.extend(f)

        chopped_arguments = zip(chop(macros, _pools), chop(files, _pools))
        chopped_filenames = Parallel(n_jobs=_pools)(delayed(fijibin.macro.run)
                                      (macro=arg[0], output_files=arg[1])
                                      for arg in chopped_arguments)

        # flatten
        return [f for list_ in chopped_filenames for f in list_]