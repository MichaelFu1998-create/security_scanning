def _validate_subjects(cursor, model):
    """Give a database cursor and model, check the subjects against
    the subject vocabulary.
    """
    subject_vocab = [term[0] for term in acquire_subject_vocabulary(cursor)]
    subjects = model.metadata.get('subjects', [])
    invalid_subjects = [s for s in subjects if s not in subject_vocab]
    if invalid_subjects:
        raise exceptions.InvalidMetadata('subjects', invalid_subjects)