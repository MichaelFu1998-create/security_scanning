def lab_dump(ann, comment, filename, sep, comment_char):
    '''Save an annotation as a lab/csv.

    Parameters
    ----------
    ann : Annotation
        The annotation object

    comment : str
        The comment string header

    filename : str
        The output filename

    sep : str
        The separator string for output

    comment_char : str
        The character used to denote comments
    '''

    intervals, values = ann.to_interval_values()

    frame = pd.DataFrame(columns=['Time', 'End Time', 'Label'],
                         data={'Time': intervals[:, 0],
                               'End Time': intervals[:, 1],
                               'Label': values})

    with open(filename, 'w') as fdesc:
        for line in comment.split('\n'):
            fdesc.write('{:s}  {:s}\n'.format(comment_char, line))

        frame.to_csv(path_or_buf=fdesc, index=False, sep=sep)