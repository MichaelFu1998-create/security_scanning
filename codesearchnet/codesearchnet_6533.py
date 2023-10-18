def _get_available_choices(self, queryset, value):
        """
        get possible choices for selection
        """
        item = queryset.filter(pk=value).first()
        if item:
            try:
                pk = getattr(item, self.chained_model_field + "_id")
                filter = {self.chained_model_field: pk}
            except AttributeError:
                try:  # maybe m2m?
                    pks = getattr(item, self.chained_model_field).all().values_list('pk', flat=True)
                    filter = {self.chained_model_field + "__in": pks}
                except AttributeError:
                    try:  # maybe a set?
                        pks = getattr(item, self.chained_model_field + "_set").all().values_list('pk', flat=True)
                        filter = {self.chained_model_field + "__in": pks}
                    except AttributeError:  # give up
                        filter = {}
            filtered = list(get_model(self.to_app_name, self.to_model_name).objects.filter(**filter).distinct())
            if self.sort:
                sort_results(filtered)
        else:
            # invalid value for queryset
            filtered = []

        return filtered