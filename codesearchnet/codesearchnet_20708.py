def move_to_folder(self, folder_path, groupby_field_name=None):
        """Copy the file groups to folder_path. Each group will be copied into
        a subfolder with named given by groupby_field.

        Parameters
        ----------
        folder_path: str
         Path to where copy the DICOM files.

        groupby_field_name: str
         DICOM field name. Will get the value of this field to name the group
         folder. If empty or None will use the basename of the group key file.
        """
        try:
            copy_groups_to_folder(self.dicom_groups, folder_path, groupby_field_name)
        except IOError as ioe:
            raise IOError('Error moving dicom groups to {}.'.format(folder_path)) from ioe