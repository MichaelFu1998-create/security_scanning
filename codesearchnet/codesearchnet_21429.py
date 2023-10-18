def build_index_and_mapping(triples):
    """index all triples into indexes and return their mappings"""
    ents = bidict()
    rels = bidict()
    ent_id = 0
    rel_id = 0

    collected = []
    for t in triples:
        for e in (t.head, t.tail):
            if e not in ents:
                ents[e] = ent_id
                ent_id += 1
        if t.relation not in rels:
            rels[t.relation] = rel_id
            rel_id += 1
        collected.append(kgedata.TripleIndex(ents[t.head], rels[t.relation], ents[t.tail]))

    return collected, ents, rels