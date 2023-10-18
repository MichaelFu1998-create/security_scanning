def _multiple_self_ref_fk_check(class_model):
    """
    We check whether a class has more than 1 FK reference to itself.
    """
    self_fk = []
    for f in class_model._meta.concrete_fields:
        if f.related_model in self_fk:
            return True
        if f.related_model == class_model:
            self_fk.append(class_model)
    return False