def bulge_disk_tag_from_align_bulge_disks(align_bulge_disk_centre, align_bulge_disk_axis_ratio, align_bulge_disk_phi):
    """Generate a tag for the alignment of the geometry of the bulge and disk of a bulge-disk system, to customize \ 
    phase names based on the bulge-disk model. This adds together the bulge_disk tags generated in the 3 functions
    above
    """
    align_bulge_disk_centre_tag = align_bulge_disk_centre_tag_from_align_bulge_disk_centre(
        align_bulge_disk_centre=align_bulge_disk_centre)
    align_bulge_disk_axis_ratio_tag = align_bulge_disk_axis_ratio_tag_from_align_bulge_disk_axis_ratio(
        align_bulge_disk_axis_ratio=align_bulge_disk_axis_ratio)
    align_bulge_disk_phi_tag = align_bulge_disk_phi_tag_from_align_bulge_disk_phi(
        align_bulge_disk_phi=align_bulge_disk_phi)

    return align_bulge_disk_centre_tag + align_bulge_disk_axis_ratio_tag + align_bulge_disk_phi_tag