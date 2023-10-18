def strip_labels(filename):
    """Strips labels."""
    labels = []
    with open(filename) as f, open('processed_labels.txt', 'w') as f1:
        for l in f:
            if l.startswith('#'):
                next
            l = l.replace(" .", '')
            l = l.replace(">\tskos:prefLabel\t", ' ')
            l = l.replace("<", '')
            l = l.replace(">\trdfs:label\t", ' ')
            f1.write(l)