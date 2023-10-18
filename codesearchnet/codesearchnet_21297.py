def write_triples(filename, triples, delimiter=DEFAULT_DELIMITER, triple_order="hrt"):
    """write triples to file."""
    with open(filename, 'w') as f:
        for t in triples:
            line = t.serialize(delimiter, triple_order)
            f.write(line + "\n")