def _thumbnail_div(full_dir, fname, snippet, is_backref=False):
    """Generates RST to place a thumbnail in a gallery"""
    thumb = os.path.join(full_dir, 'images', 'thumb',
                         'sphx_glr_%s_thumb.png' % fname[:-3])
    ref_name = os.path.join(full_dir, fname).replace(os.path.sep, '_')

    template = BACKREF_THUMBNAIL_TEMPLATE if is_backref else THUMBNAIL_TEMPLATE
    return template.format(snippet=snippet, thumbnail=thumb, ref_name=ref_name)