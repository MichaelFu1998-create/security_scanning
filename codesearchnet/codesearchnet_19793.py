def fasta_dict_to_file(fasta_dict, fasta_file, line_char_limit=None):
    """Write fasta_dict to fasta_file

    :param fasta_dict: returned by fasta_file_to_dict
    :param fasta_file: output file can be a string path or a file object
    :param line_char_limit: None = no limit (default)
    :return: None
    """
    fasta_fp = fasta_file
    if isinstance(fasta_file, str):
        fasta_fp = open(fasta_file, 'wb')

    for key in fasta_dict:
        seq = fasta_dict[key]['seq']
        if line_char_limit:
            seq = '\n'.join([seq[i:i+line_char_limit] for i in range(0, len(seq), line_char_limit)])
        fasta_fp.write(u'{0:s}\n{1:s}\n'.format(fasta_dict[key]['header'], seq))