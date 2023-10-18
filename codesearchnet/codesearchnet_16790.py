def index_particles(particles):
    """Indexes :class:`Particle` objects.  It returns a regex pattern which
    matches to any particle morphs and a dictionary indexes the given particles
    by regex groups.
    """
    patterns, indices = [], {}
    for x, p in enumerate(particles):
        group = u'_%d' % x
        indices[group] = x
        patterns.append(u'(?P<%s>%s)' % (group, p.regex_pattern()))
    pattern = re.compile(u'|'.join(patterns))
    return pattern, indices