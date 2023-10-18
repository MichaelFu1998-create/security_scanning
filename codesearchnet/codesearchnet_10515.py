def load_positions(positions_path):
    """Load the positions of an image.

    Positions correspond to a set of pixels in the lensed source galaxy that are anticipated to come from the same \
    multiply-imaged region of the source-plane. Mass models which do not trace the pixels within a threshold value of \
    one another are resampled during the non-linear search.

    Positions are stored in a .dat file, where each line of the file gives a list of list of (y,x) positions which \
    correspond to the same region of the source-plane. Thus, multiple source-plane regions can be input over multiple \
    lines of the same positions file.

    Parameters
    ----------
    positions_path : str
        The path to the positions .dat file containing the positions (e.g. '/path/to/positions.dat')
    """
    with open(positions_path) as f:
        position_string = f.readlines()

    positions = []

    for line in position_string:
        position_list = ast.literal_eval(line)
        positions.append(position_list)

    return positions