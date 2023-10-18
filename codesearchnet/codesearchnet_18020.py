def get_residuals_update_tile(st, padded_tile):
    """
    Translates a tile in the padded image to the unpadded image.

    Given a state and a tile that corresponds to the padded image, returns
    a tile that corresponds to the the corresponding pixels of the difference
    image

    Parameters
    ----------
        st : :class:`peri.states.State`
            The state
        padded_tile : :class:`peri.util.Tile`
            The tile in the padded image.

    Returns
    -------
        :class:`peri.util.Tile`
            The tile corresponding to padded_tile in the unpadded image.
    """
    inner_tile = st.ishape.intersection([st.ishape, padded_tile])
    return inner_tile.translate(-st.pad)