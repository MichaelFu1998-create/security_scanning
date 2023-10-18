def from_dict(self, subj_files):
        """
        Parameters
        ----------
        subj_files: dict of str
            file_path -> int/str
        """
        for group_label in subj_files:
            try:
                group_files = subj_files[group_label]
                self.items.extend([self._load_image(get_abspath(imgf)) for imgf in group_files])

                self.labels.extend([group_label]*len(group_files))

            except Exception as exc:
                raise Exception('Error while reading files from '
                                'group {0}.'.format(group_label)) from exc