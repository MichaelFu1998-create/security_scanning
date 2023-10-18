def get_comments(jam, ann):
    '''Get the metadata from a jam and an annotation, combined as a string.

    Parameters
    ----------
    jam : JAMS
        The jams object

    ann : Annotation
        An annotation object

    Returns
    -------
    comments : str
        The jam.file_metadata and ann.annotation_metadata, combined and serialized
    '''
    jam_comments = jam.file_metadata.__json__
    ann_comments = ann.annotation_metadata.__json__
    return json.dumps({'metadata': jam_comments,
                       'annotation metadata': ann_comments},
                      indent=2)