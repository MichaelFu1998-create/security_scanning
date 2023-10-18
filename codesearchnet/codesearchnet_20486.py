def parse_subjects_list(filepath, datadir='', split=':', labelsf=None):
    """Parses a file with a list of: <subject_file>:<subject_class_label>.

    Parameters
    ----------
    filepath: str
    Path to file with a list of: <subject_file>:<subject_class_label>.
    Where ':' can be any split character

    datadir: str
    String to be path prefix of each line of the fname content,
    only in case the lines are relative file paths.

    split: str
    Split character for each line

    labelsf: str
    Path to file with a list of the labels if it is not included in
    fname. It will overwrite the labels from fname.

    Returns
    -------
    [labels, subjs] where labels is a list of labels and subjs a list of
    filepaths
    """
    labels = []
    subjs  = []

    if datadir:
        datadir += op.sep

    with open(filepath, 'r') as f:
        for s in f:
            line = s.strip().split(split)
            if len(line) == 2:
                labels.append(np.float(line[1]))
                subjf = line[0].strip()
            else:
                subjf = line.strip()

            if not op.isabs(subjf):
                subjs.append(datadir + subjf)
            else:
                subjs.append(subjf)


    if labelsf is not None:
        labels = np.loadtxt(labelsf)

    return [labels, subjs]