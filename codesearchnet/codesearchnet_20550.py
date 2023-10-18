def from_list(self, subj_files):
        """
        Parameters
        ----------
        subj_files: list of str
            file_paths
        """
        for sf in subj_files:
            try:
                nii_img = self._load_image(get_abspath(sf))
                self.items.append(nii_img)
            except Exception as exc:
                raise Exception('Error while reading file {0}.'.format(sf)) from exc