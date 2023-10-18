def write_index_translation(translation_filename, entity_ids, relation_ids):
    """write triples into a translation file."""
    translation = triple_pb.Translation()
    entities = []
    for name, index in entity_ids.items():
        translation.entities.add(element=name, index=index)
    relations = []
    for name, index in relation_ids.items():
        translation.relations.add(element=name, index=index)
    with open(translation_filename, "wb") as f:
        f.write(translation.SerializeToString())