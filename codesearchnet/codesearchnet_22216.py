def all_comments(self):
        """
        Returns combined list of event and update comments.
        """
        ctype = ContentType.objects.get(app_label__exact="happenings", model__exact='event')
        update_ctype = ContentType.objects.get(app_label__exact="happenings", model__exact='update')
        update_ids = self.update_set.values_list('id', flat=True)

        return Comment.objects.filter(
            Q(content_type=ctype.id, object_pk=self.id) |
            Q(content_type=update_ctype.id, object_pk__in=update_ids)
        )