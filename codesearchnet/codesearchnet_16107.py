def get_encrypted_field(base_class):
    """
    A get or create method for encrypted fields, we cache the field in
    the module to avoid recreation. This also allows us to always return
    the same class reference for a field.

    :type base_class: models.Field[T]
    :rtype: models.Field[EncryptedMixin, T]
    """
    assert not isinstance(base_class, models.Field)
    field_name = 'Encrypted' + base_class.__name__
    if base_class not in FIELD_CACHE:
        FIELD_CACHE[base_class] = type(field_name,
                                       (EncryptedMixin, base_class), {
                                           'base_class': base_class,
                                       })
    return FIELD_CACHE[base_class]