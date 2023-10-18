def get_field_names(obj, ignore_auto=True, ignore_relations=True, 
        exclude=[]):
    """Returns the field names of a Django model object.

    :param obj: the Django model class or object instance to get the fields
        from
    :param ignore_auto: ignore any fields of type AutoField. Defaults to True
    :param ignore_relations: ignore any fields that involve relations such as
        the ForeignKey or ManyToManyField
    :param exclude: exclude anything in this list from the results

    :returns: generator of found field names
    """

    from django.db.models import (AutoField, ForeignKey, ManyToManyField, 
        ManyToOneRel, OneToOneField, OneToOneRel)

    for field in obj._meta.get_fields():
        if ignore_auto and isinstance(field, AutoField):
            continue

        if ignore_relations and (isinstance(field, ForeignKey) or
                isinstance(field, ManyToManyField) or
                isinstance(field, ManyToOneRel) or
                isinstance(field, OneToOneRel) or
                isinstance(field, OneToOneField)):
            # optimization is killing coverage measure, have to put no-op that
            # does something
            a = 1; a
            continue

        if field.name in exclude:
            continue

        yield field.name