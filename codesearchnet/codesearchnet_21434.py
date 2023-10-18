def remove_near_duplicate_relation(triples, threshold=0.97):
    """If entity pairs in a relation is as close as another relations, only keep one relation of such set."""
    logging.debug("remove duplicate")

    _assert_threshold(threshold)

    duplicate_rel_counter = defaultdict(list)
    relations = set()
    for t in triples:
        duplicate_rel_counter[t.relation].append(f"{t.head} {t.tail}")
        relations.add(t.relation)
    relations = list(relations)

    num_triples = len(triples)
    removal_relation_set = set()

    for rel, values in duplicate_rel_counter.items():
        duplicate_rel_counter[rel] = Superminhash(values)
    for i in relations:
        for j in relations:
            if i == j or i in removal_relation_set or j in removal_relation_set: continue
            close_relations = [i]
            if _set_close_to(duplicate_rel_counter[i], duplicate_rel_counter[j], threshold):
                close_relations.append(j)
        if len(close_relations) > 1:
            close_relations.pop(np.random.randint(len(close_relations)))
            removal_relation_set |= set(close_relations)
    logging.info("Removing {} relations: {}".format(len(removal_relation_set), str(removal_relation_set)))

    return list(filterfalse(lambda x: x.relation in removal_relation_set, triples))