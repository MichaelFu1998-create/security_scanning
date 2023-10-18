def _init_subj_data(self, subj_files):
        """
        Parameters
        ----------
        subj_files: list or dict of str
            file_path -> int/str
        """
        try:
            if isinstance(subj_files, list):
                self.from_list(subj_files)

            elif isinstance(subj_files, dict):
                self.from_dict(subj_files)
            else:
                raise ValueError('Could not recognize subj_files argument variable type.')
        except Exception as exc:
            raise Exception('Cannot read subj_files input argument.') from exc