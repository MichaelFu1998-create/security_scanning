def _deserialize_store_model(self, fk_cache):
        """
        When deserializing a store model, we look at the deleted flags to know if we should delete the app model.
        Upon loading the app model in memory we validate the app models fields, if any errors occurs we follow
        foreign key relationships to see if the related model has been deleted to propagate that deletion to the target app model.
        We return:
        None => if the model was deleted successfully
        model => if the model validates successfully
        """
        klass_model = _profile_models[self.profile][self.model_name]
        # if store model marked as deleted, attempt to delete in app layer
        if self.deleted:
            # if hard deleted, propagate to related models
            if self.hard_deleted:
                try:
                    klass_model.objects.get(id=self.id).delete(hard_delete=True)
                except klass_model.DoesNotExist:
                    pass
            else:
                klass_model.objects.filter(id=self.id).delete()
            return None
        else:
            # load model into memory
            app_model = klass_model.deserialize(json.loads(self.serialized))
            app_model._morango_source_id = self.source_id
            app_model._morango_partition = self.partition
            app_model._morango_dirty_bit = False

            try:
                # validate and return the model
                app_model.cached_clean_fields(fk_cache)
                return app_model
            except exceptions.ValidationError as e:
                logger.warn("Validation error for {model} with id {id}: {error}".format(model=klass_model.__name__, id=app_model.id, error=e))
                # check FKs in store to see if any of those models were deleted or hard_deleted to propagate to this model
                fk_ids = [getattr(app_model, field.attname) for field in app_model._meta.fields if isinstance(field, ForeignKey)]
                for fk_id in fk_ids:
                    try:
                        st_model = Store.objects.get(id=fk_id)
                        if st_model.deleted:
                            # if hard deleted, propagate to store model
                            if st_model.hard_deleted:
                                app_model._update_hard_deleted_models()
                            app_model._update_deleted_models()
                            return None
                    except Store.DoesNotExist:
                        pass
                raise e