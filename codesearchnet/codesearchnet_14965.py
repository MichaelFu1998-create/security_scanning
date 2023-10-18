def _deserialize_from_store(profile):
    """
    Takes data from the store and integrates into the application.
    """
    # we first serialize to avoid deserialization merge conflicts
    _serialize_into_store(profile)

    fk_cache = {}
    with transaction.atomic():
        syncable_dict = _profile_models[profile]
        excluded_list = []
        # iterate through classes which are in foreign key dependency order
        for model_name, klass_model in six.iteritems(syncable_dict):
            # handle cases where a class has a single FK reference to itself
            self_ref_fk = _self_referential_fk(klass_model)
            query = Q(model_name=klass_model.morango_model_name)
            for klass in klass_model.morango_model_dependencies:
                query |= Q(model_name=klass.morango_model_name)
            if self_ref_fk:
                clean_parents = Store.objects.filter(dirty_bit=False, profile=profile).filter(query).char_ids_list()
                dirty_children = Store.objects.filter(dirty_bit=True, profile=profile) \
                                              .filter(Q(_self_ref_fk__in=clean_parents) | Q(_self_ref_fk='')).filter(query)

                # keep iterating until size of dirty_children is 0
                while len(dirty_children) > 0:
                    for store_model in dirty_children:
                        try:
                            app_model = store_model._deserialize_store_model(fk_cache)
                            if app_model:
                                with mute_signals(signals.pre_save, signals.post_save):
                                    app_model.save(update_dirty_bit_to=False)
                            # we update a store model after we have deserialized it to be able to mark it as a clean parent
                            store_model.dirty_bit = False
                            store_model.save(update_fields=['dirty_bit'])
                        except exceptions.ValidationError:
                            # if the app model did not validate, we leave the store dirty bit set
                            excluded_list.append(store_model.id)

                    # update lists with new clean parents and dirty children
                    clean_parents = Store.objects.filter(dirty_bit=False, profile=profile).filter(query).char_ids_list()
                    dirty_children = Store.objects.filter(dirty_bit=True, profile=profile, _self_ref_fk__in=clean_parents).filter(query)
            else:
                # array for holding db values from the fields of each model for this class
                db_values = []
                fields = klass_model._meta.fields
                for store_model in Store.objects.filter(model_name=model_name, profile=profile, dirty_bit=True):
                    try:
                        app_model = store_model._deserialize_store_model(fk_cache)
                        # if the model was not deleted add its field values to the list
                        if app_model:
                            for f in fields:
                                value = getattr(app_model, f.attname)
                                db_value = f.get_db_prep_value(value, connection)
                                db_values.append(db_value)
                    except exceptions.ValidationError:
                        # if the app model did not validate, we leave the store dirty bit set
                        excluded_list.append(store_model.id)

                if db_values:
                    # number of rows to update
                    num_of_rows = len(db_values) // len(fields)
                    # create '%s' placeholders for a single row
                    placeholder_tuple = tuple(['%s' for _ in range(len(fields))])
                    # create list of the '%s' tuple placeholders based on number of rows to update
                    placeholder_list = [str(placeholder_tuple) for _ in range(num_of_rows)]
                    with connection.cursor() as cursor:
                        DBBackend._bulk_insert_into_app_models(cursor, klass_model._meta.db_table, fields, db_values, placeholder_list)

        # clear dirty bit for all store models for this profile except for models that did not validate
        Store.objects.exclude(id__in=excluded_list).filter(profile=profile, dirty_bit=True).update(dirty_bit=False)