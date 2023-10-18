def _serialize_into_store(profile, filter=None):
    """
    Takes data from app layer and serializes the models into the store.
    """
    # ensure that we write and retrieve the counter in one go for consistency
    current_id = InstanceIDModel.get_current_instance_and_increment_counter()

    with transaction.atomic():
        # create Q objects for filtering by prefixes
        prefix_condition = None
        if filter:
            prefix_condition = functools.reduce(lambda x, y: x | y, [Q(_morango_partition__startswith=prefix) for prefix in filter])

        # filter through all models with the dirty bit turned on
        syncable_dict = _profile_models[profile]
        for (_, klass_model) in six.iteritems(syncable_dict):
            new_store_records = []
            new_rmc_records = []
            klass_queryset = klass_model.objects.filter(_morango_dirty_bit=True)
            if prefix_condition:
                klass_queryset = klass_queryset.filter(prefix_condition)
            store_records_dict = Store.objects.in_bulk(id_list=klass_queryset.values_list('id', flat=True))
            for app_model in klass_queryset:
                try:
                    store_model = store_records_dict[app_model.id]

                    # if store record dirty and app record dirty, append store serialized to conflicting data
                    if store_model.dirty_bit:
                        store_model.conflicting_serialized_data = store_model.serialized + "\n" + store_model.conflicting_serialized_data
                        store_model.dirty_bit = False

                    # set new serialized data on this store model
                    ser_dict = json.loads(store_model.serialized)
                    ser_dict.update(app_model.serialize())
                    store_model.serialized = DjangoJSONEncoder().encode(ser_dict)

                    # create or update instance and counter on the record max counter for this store model
                    RecordMaxCounter.objects.update_or_create(defaults={'counter': current_id.counter},
                                                              instance_id=current_id.id,
                                                              store_model_id=store_model.id)

                    # update last saved bys for this store model
                    store_model.last_saved_instance = current_id.id
                    store_model.last_saved_counter = current_id.counter
                    # update deleted flags in case it was previously deleted
                    store_model.deleted = False
                    store_model.hard_deleted = False

                    # update this model
                    store_model.save()

                except KeyError:
                    kwargs = {
                        'id': app_model.id,
                        'serialized': DjangoJSONEncoder().encode(app_model.serialize()),
                        'last_saved_instance': current_id.id,
                        'last_saved_counter': current_id.counter,
                        'model_name': app_model.morango_model_name,
                        'profile': app_model.morango_profile,
                        'partition': app_model._morango_partition,
                        'source_id': app_model._morango_source_id,
                    }
                    # check if model has FK pointing to it and add the value to a field on the store
                    self_ref_fk = _self_referential_fk(klass_model)
                    if self_ref_fk:
                        self_ref_fk_value = getattr(app_model, self_ref_fk)
                        kwargs.update({'_self_ref_fk': self_ref_fk_value or ''})
                    # create store model and record max counter for the app model
                    new_store_records.append(Store(**kwargs))
                    new_rmc_records.append(RecordMaxCounter(store_model_id=app_model.id, instance_id=current_id.id, counter=current_id.counter))

            # bulk create store and rmc records for this class
            Store.objects.bulk_create(new_store_records)
            RecordMaxCounter.objects.bulk_create(new_rmc_records)

            # set dirty bit to false for all instances of this model
            klass_queryset.update(update_dirty_bit_to=False)

        # get list of ids of deleted models
        deleted_ids = DeletedModels.objects.filter(profile=profile).values_list('id', flat=True)
        # update last_saved_bys and deleted flag of all deleted store model instances
        deleted_store_records = Store.objects.filter(id__in=deleted_ids)
        deleted_store_records.update(dirty_bit=False, deleted=True, last_saved_instance=current_id.id, last_saved_counter=current_id.counter)
        # update rmcs counters for deleted models that have our instance id
        RecordMaxCounter.objects.filter(instance_id=current_id.id, store_model_id__in=deleted_ids).update(counter=current_id.counter)
        # get a list of deleted model ids that don't have an rmc for our instance id
        new_rmc_ids = deleted_store_records.exclude(recordmaxcounter__instance_id=current_id.id).values_list("id", flat=True)
        # bulk create these new rmcs
        RecordMaxCounter.objects.bulk_create([RecordMaxCounter(store_model_id=r_id, instance_id=current_id.id, counter=current_id.counter) for r_id in new_rmc_ids])
        # clear deleted models table for this profile
        DeletedModels.objects.filter(profile=profile).delete()

        # handle logic for hard deletion models
        hard_deleted_ids = HardDeletedModels.objects.filter(profile=profile).values_list('id', flat=True)
        hard_deleted_store_records = Store.objects.filter(id__in=hard_deleted_ids)
        hard_deleted_store_records.update(hard_deleted=True, serialized='{}', conflicting_serialized_data='')
        HardDeletedModels.objects.filter(profile=profile).delete()

        # update our own database max counters after serialization
        if not filter:
            DatabaseMaxCounter.objects.update_or_create(instance_id=current_id.id, partition="", defaults={'counter': current_id.counter})
        else:
            for f in filter:
                DatabaseMaxCounter.objects.update_or_create(instance_id=current_id.id, partition=f, defaults={'counter': current_id.counter})