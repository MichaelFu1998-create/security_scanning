def create_input_peptides_files(
        peptides,
        max_peptides_per_file=None,
        group_by_length=False):
    """
    Creates one or more files containing one peptide per line,
    returns names of files.
    """
    if group_by_length:
        peptide_lengths = {len(p) for p in peptides}
        peptide_groups = {l: [] for l in peptide_lengths}
        for p in peptides:
            peptide_groups[len(p)].append(p)
    else:
        peptide_groups = {"": peptides}

    file_names = []
    for key, group in peptide_groups.items():
        n_peptides = len(group)
        if not max_peptides_per_file:
            max_peptides_per_file = n_peptides
        input_file = None
        for i, p in enumerate(group):
            if i % max_peptides_per_file == 0:
                if input_file is not None:
                    file_names.append(input_file.name)
                    input_file.close()
                input_file = make_writable_tempfile(
                    prefix_number=i // max_peptides_per_file,
                    prefix_name=key,
                    suffix=".txt")
            input_file.write("%s\n" % p)
        if input_file is not None:
            file_names.append(input_file.name)
            input_file.close()
    return file_names