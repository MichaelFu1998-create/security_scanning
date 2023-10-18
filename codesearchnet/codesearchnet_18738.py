def register_field(cls, field):
    """
    Handles registering the fields with the FieldRegistry and creating a 
    post-save signal for the model.
    """
    FieldRegistry.add_field(cls, field)
    
    signals.post_save.connect(handle_save_embeds, sender=cls,
            dispatch_uid='%s.%s.%s' % \
            (cls._meta.app_label, cls._meta.module_name, field.name))