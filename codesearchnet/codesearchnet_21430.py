def recover_triples_from_mapping(indexes, ents: bidict, rels: bidict):
    """recover triples from mapping."""
    triples = []
    for t in indexes:
        triples.append(kgedata.Triple(ents.inverse[t.head], rels.inverse[t.relation], ents.inverse[t.tail]))
    return triples