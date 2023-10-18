def convert_jams(jams_file, output_prefix, csv=False, comment_char='#', namespaces=None):
    '''Convert jams to labs.

    Parameters
    ----------
    jams_file : str
        The path on disk to the jams file in question

    output_prefix : str
        The file path prefix of the outputs

    csv : bool
        Whether to output in csv (True) or lab (False) format

    comment_char : str
        The character used to denote comments

    namespaces : list-like
        The set of namespace patterns to match for output
    '''

    if namespaces is None:
        raise ValueError('No namespaces provided. Try ".*" for all namespaces.')

    jam = jams.load(jams_file)

    # Get all the annotations
    # Filter down to the unique ones
    # For each annotation
    #     generate the comment string
    #     generate the output filename
    #     dump to csv

    # Make a counter object for each namespace type
    counter = collections.Counter()

    annotations = []

    for query in namespaces:
        annotations.extend(jam.search(namespace=query))

    if csv:
        suffix = 'csv'
        sep = ','
    else:
        suffix = 'lab'
        sep = '\t'

    for ann in annotations:
        index = counter[ann.namespace]
        counter[ann.namespace] += 1
        filename = os.path.extsep.join([get_output_name(output_prefix,
                                                        ann.namespace,
                                                        index),
                                        suffix])

        comment = get_comments(jam, ann)

        # Dump to disk
        lab_dump(ann, comment, filename, sep, comment_char)