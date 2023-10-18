def apply_mask(img, mask):
    """Return the image with the given `mask` applied."""
    from .mask import apply_mask

    vol, _ = apply_mask(img, mask)
    return vector_to_volume(vol, read_img(mask).get_data().astype(bool))