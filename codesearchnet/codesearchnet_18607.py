def invalidate_stored_oembeds(self, sender, instance, created, **kwargs):
        """
        A hook for django-based oembed providers to delete any stored oembeds
        """
        ctype = ContentType.objects.get_for_model(instance)
        StoredOEmbed.objects.filter(
            object_id=instance.pk,
            content_type=ctype).delete()