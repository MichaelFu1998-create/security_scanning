def aux_listing(aux_root):
    """Listing"""

    listing = []

    for root, _, fnames in os.walk(aux_root):
        count = len(aux_root.split(os.sep))
        prefix = root.split(os.sep)[count:]

        for fname in fnames:
            listing.append(os.sep.join(prefix + [fname]))

    return listing