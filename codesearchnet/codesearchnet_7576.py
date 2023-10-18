def save_thumbnail(image_path, base_image_name, gallery_conf):
    """Save the thumbnail image"""
    first_image_file = image_path.format(1)
    thumb_dir = os.path.join(os.path.dirname(first_image_file), 'thumb')
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)

    thumb_file = os.path.join(thumb_dir,
                              'sphx_glr_%s_thumb.png' % base_image_name)

    if os.path.exists(first_image_file):
        scale_image(first_image_file, thumb_file, 400, 280)
    elif not os.path.exists(thumb_file):
        # create something to replace the thumbnail
        default_thumb_file = os.path.join(glr_path_static(), 'no_image.png')
        default_thumb_file = gallery_conf.get("default_thumb_file",
                                              default_thumb_file)
        scale_image(default_thumb_file, thumb_file, 200, 140)