def add_syncable_models():
    """
    Per profile, adds each model to a dictionary mapping the morango model name to its model class.
    We sort by ForeignKey dependencies to safely sync data.
    """

    import django.apps
    from morango.models import SyncableModel
    from morango.manager import SyncableModelManager
    from morango.query import SyncableModelQuerySet

    model_list = []
    for model_class in django.apps.apps.get_models():
        # several validation checks to assert models will be syncing correctly
        if issubclass(model_class, SyncableModel):
            name = model_class.__name__
            if _multiple_self_ref_fk_check(model_class):
                raise InvalidMorangoModelConfiguration("Syncing models with more than 1 self referential ForeignKey is not supported.")
            try:
                from mptt import models
                from morango.utils.morango_mptt import MorangoMPTTModel, MorangoMPTTTreeManager, MorangoTreeQuerySet
                # mptt syncable model checks
                if issubclass(model_class, models.MPTTModel):
                    if not issubclass(model_class, MorangoMPTTModel):
                        raise InvalidMorangoModelConfiguration("{} that inherits from MPTTModel, should instead inherit from MorangoMPTTModel.".format(name))
                    if not isinstance(model_class.objects, MorangoMPTTTreeManager):
                        raise InvalidMPTTManager("Manager for {} must inherit from MorangoMPTTTreeManager.".format(name))
                    if not isinstance(model_class.objects.none(), MorangoTreeQuerySet):
                        raise InvalidMPTTQuerySet("Queryset for {} model must inherit from MorangoTreeQuerySet.".format(name))
            except ImportError:
                pass
            # syncable model checks
            if not isinstance(model_class.objects, SyncableModelManager):
                raise InvalidSyncableManager("Manager for {} must inherit from SyncableModelManager.".format(name))
            if not isinstance(model_class.objects.none(), SyncableModelQuerySet):
                raise InvalidSyncableQueryset("Queryset for {} model must inherit from SyncableModelQuerySet.".format(name))
            if model_class._meta.many_to_many:
                raise UnsupportedFieldType("{} model with a ManyToManyField is not supported in morango.")
            if not hasattr(model_class, 'morango_model_name'):
                raise InvalidMorangoModelConfiguration("{} model must define a morango_model_name attribute".format(name))
            if not hasattr(model_class, 'morango_profile'):
                raise InvalidMorangoModelConfiguration("{} model must define a morango_profile attribute".format(name))

            # create empty list to hold model classes for profile if not yet created
            profile = model_class.morango_profile
            _profile_models[profile] = _profile_models.get(profile, [])

            # don't sync models where morango_model_name is None
            if model_class.morango_model_name is not None:
                _insert_model_into_profile_dict(model_class, profile)

    # for each profile, create a dict mapping from morango model names to model class
    for profile, model_list in iteritems(_profile_models):
        syncable_models_dict = OrderedDict()
        for model_class in model_list:
            syncable_models_dict[model_class.morango_model_name] = model_class
        _profile_models[profile] = syncable_models_dict