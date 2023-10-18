def video_size(source, converter='ffmpeg'):
    """Returns the dimensions of the video."""

    res = subprocess.run([converter, '-i', source], stderr=subprocess.PIPE)
    stderr = res.stderr.decode('utf8')
    pattern = re.compile(r'Stream.*Video.* ([0-9]+)x([0-9]+)')
    match = pattern.search(stderr)
    rot_pattern = re.compile(r'rotate\s*:\s*-?(90|270)')
    rot_match = rot_pattern.search(stderr)

    if match:
        x, y = int(match.groups()[0]), int(match.groups()[1])
    else:
        x = y = 0
    if rot_match:
        x, y = y, x
    return x, y