def get_groups_in_same_folder(self, folder_depth=3):
        """
        Returns a list of 2-tuples with pairs of dicom groups that
        are in the same folder within given depth.

        Parameters
        ----------
        folder_depth: int
        Path depth to check for folder equality.

        Returns
        -------
        list of tuples of str
        """
        group_pairs = []
        key_dicoms = list(self.dicom_groups.keys())
        idx = len(key_dicoms)
        while idx > 0:
            group1 = key_dicoms.pop()
            dir_group1 = get_folder_subpath(group1, folder_depth)
            for group in key_dicoms:
                if group.startswith(dir_group1):
                    group_pairs.append((group1, group))
            idx -= 1

        return group_pairs