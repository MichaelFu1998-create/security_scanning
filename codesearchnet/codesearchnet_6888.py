def load_group_assignments_DDBST():
    '''Data is stored in the format
    InChI key\tbool bool bool \tsubgroup count ...\tsubgroup count \tsubgroup count...
    where the bools refer to whether or not the original UNIFAC, modified
    UNIFAC, and PSRK group assignments were completed correctly.
    The subgroups and their count have an indefinite length.
    '''
    # Do not allow running multiple times
    if DDBST_UNIFAC_assignments:
        return None
    with open(os.path.join(folder, 'DDBST UNIFAC assignments.tsv')) as f:
        _group_assignments = [DDBST_UNIFAC_assignments, DDBST_MODIFIED_UNIFAC_assignments, DDBST_PSRK_assignments]
        for line in f.readlines():
            key, valids, original, modified, PSRK = line.split('\t')
            # list of whether or not each method was correctly identified or not
            valids = [True if i == '1' else False for i in valids.split(' ')]
            for groups, storage, valid in zip([original, modified, PSRK], _group_assignments, valids):
                if valid:
                    groups = groups.rstrip().split(' ')
                    d_data = {}
                    for i in range(int(len(groups)/2)):
                        d_data[int(groups[i*2])] = int(groups[i*2+1])
                    storage[key] = d_data