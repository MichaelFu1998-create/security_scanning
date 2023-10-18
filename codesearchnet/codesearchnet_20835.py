def parse_amc(source):
    '''Parse an AMC motion capture data file.

    Parameters
    ----------
    source : file
        A file-like object that contains AMC motion capture text.

    Yields
    ------
    frame : dict
        Yields a series of motion capture frames. Each frame is a dictionary
        that maps a bone name to a list of the DOF configurations for that bone.
    '''
    lines = 0
    frames = 1
    frame = {}
    degrees = False
    for line in source:
        lines += 1
        line = line.split('#')[0].strip()
        if not line:
            continue
        if line.startswith(':'):
            if line.lower().startswith(':deg'):
                degrees = True
            continue
        if line.isdigit():
            if int(line) != frames:
                raise RuntimeError(
                    'frame mismatch on line {}: '
                    'produced {} but file claims {}'.format(lines, frames, line))
            yield frame
            frames += 1
            frame = {}
            continue
        fields = line.split()
        frame[fields[0]] = list(map(float, fields[1:]))