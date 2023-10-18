def copy_groups_to_folder(dicom_groups, folder_path, groupby_field_name):
    """Copy the DICOM file groups to folder_path. Each group will be copied into
    a subfolder with named given by groupby_field.

    Parameters
    ----------
    dicom_groups: boyle.dicom.sets.DicomFileSet

    folder_path: str
     Path to where copy the DICOM files.

    groupby_field_name: str
     DICOM field name. Will get the value of this field to name the group
     folder.
    """
    if dicom_groups is None or not dicom_groups:
        raise ValueError('Expected a boyle.dicom.sets.DicomFileSet.')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=False)

    for dcmg in dicom_groups:
        if groupby_field_name is not None and len(groupby_field_name) > 0:
            dfile = DicomFile(dcmg)
            dir_name = ''
            for att in groupby_field_name:
                dir_name = os.path.join(dir_name, dfile.get_attributes(att))
            dir_name = str(dir_name)
        else:
            dir_name = os.path.basename(dcmg)

        group_folder = os.path.join(folder_path, dir_name)
        os.makedirs(group_folder, exist_ok=False)

        log.debug('Copying files to {}.'.format(group_folder))

        import shutil
        dcm_files = dicom_groups[dcmg]

        for srcf in dcm_files:
            destf = os.path.join(group_folder, os.path.basename(srcf))
            while os.path.exists(destf):
                destf += '+'
            shutil.copy2(srcf, destf)