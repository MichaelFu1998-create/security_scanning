def _plots_are_current(src_file, image_file):
    """Test existence of image file and no change in md5sum of
    example"""

    first_image_file = image_file.format(1)
    has_image = os.path.exists(first_image_file)
    src_file_changed = check_md5sum_change(src_file)

    return has_image and not src_file_changed