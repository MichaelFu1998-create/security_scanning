def copy_files_to_other_folder(self, output_folder, rename_files=True,
                                   mkdir=True, verbose=False):
        """
        Copies all files within this set to the output_folder

        Parameters
        ----------
        output_folder: str
        Path of the destination folder of the files

        rename_files: bool
        Whether or not rename the files to a sequential format

        mkdir: bool
        Whether to make the folder if it does not exist

        verbose: bool
        Whether to print to stdout the files that are beind copied
        """
        import shutil

        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        if not rename_files:
            for dcmf in self.items:
                outf = os.path.join(output_folder, os.path.basename(dcmf))
                if verbose:
                    print('{} -> {}'.format(dcmf, outf))
                shutil.copyfile(dcmf, outf)
        else:
            n_pad = len(self.items)+2
            for idx, dcmf in enumerate(self.items):
                outf = '{number:0{width}d}.dcm'.format(width=n_pad, number=idx)
                outf = os.path.join(output_folder, outf)
                if verbose:
                    print('{} -> {}'.format(dcmf, outf))
                shutil.copyfile(dcmf, outf)