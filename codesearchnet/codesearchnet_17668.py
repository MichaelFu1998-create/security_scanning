def write_compound_to_auxi_file(directory, compound):
    """
    Writes a compound to an auxi file at the specified directory.

    :param dir: The directory.
    :param compound: The compound.
    """

    file_name = "Compound_" + compound.formula + ".json"
    with open(os.path.join(directory, file_name), 'w') as f:
        f.write(str(compound))