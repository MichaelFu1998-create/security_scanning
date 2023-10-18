def raise_exception(entity_type, entity, exception):
    """ Exception helper """
    raise exception(
        u'The {} you have provided is not valid: {}'.format(entity_type, entity).encode('utf-8')
    )