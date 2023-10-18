def create_subjects_file(filelist, labels, output_file, split=':'):
    """Creates a file where each line is <subject_file>:<subject_class_label>.

    Parameters
    ----------
    filelist: list of str
    List of filepaths

    labels: list of int, str or labels that can be transformed with str()
    List of labels

    output_file: str
    Output file path

    split: str
    Split character for each line

    """
    if len(filelist) != len(labels):
        raise ValueError('Expected `filelist` and `labels` to have the same length.'
                         'Got {} and {}.'.format(len(filelist), len(labels)))

    lines = []
    for i, subj in enumerate(filelist):
        lab  = labels[i]
        line = subj + split + str(lab)
        lines.append(line)

    lines = np.array(lines)
    np.savetxt(output_file, lines, fmt='%s')