def stats_from_fai(infile):
    '''Returns dictionary of length stats from an fai file. Keys are: longest, shortest, mean, total_length, N50, number'''
    f = utils.open_file_read(infile)
    try:
        lengths = sorted([int(line.split('\t')[1]) for line in f], reverse=True)
    except:
        raise Error('Error getting lengths from fai file ' + infile)
    utils.close(f)

    stats = {}
    if len(lengths) > 0:
        stats['longest'] = max(lengths)
        stats['shortest'] = min(lengths)
        stats['total_length'] = sum(lengths)
        stats['mean'] = stats['total_length'] / len(lengths)
        stats['number'] = len(lengths)

        cumulative_length = 0
        for length in lengths:
            cumulative_length += length
            if cumulative_length >= 0.5 * stats['total_length']:
                stats['N50'] = length
                break
    else:
        stats = {x: 0 for x in ('longest', 'shortest', 'mean', 'N50', 'total_length', 'number')}

    return stats