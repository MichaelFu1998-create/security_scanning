def merge_groups(self, indices):
        """Extend the lists within the DICOM groups dictionary.
        The indices will indicate which list have to be extended by which
        other list.

        Parameters
        ----------
        indices: list or tuple of 2 iterables of int, bot having the same len
             The indices of the lists that have to be merged, both iterables
             items will be read pair by pair, the first is the index to the
             list that will be extended with the list of the second index.
             The indices can be constructed with Numpy e.g.,
             indices = np.where(square_matrix)
        """
        try:
            merged = merge_dict_of_lists(self.dicom_groups, indices,
                                         pop_later=True, copy=True)
            self.dicom_groups = merged
        except IndexError:
            raise IndexError('Index out of range to merge DICOM groups.')