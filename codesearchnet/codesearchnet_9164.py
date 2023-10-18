def get_params_for_field(self, field_name, sort_type=None):
        """
        If sort_type is None - inverse current sort for field, if no sorted - use asc
        """
        if not sort_type:
            if self.initial_sort == field_name:
                sort_type = 'desc' if self.initial_sort_type == 'asc' else 'asc'
            else:
                sort_type = 'asc'
        self.initial_params[self.sort_param_name] = self.sort_fields[field_name]
        self.initial_params[self.sort_type_param_name] = sort_type
        return '?%s' % self.initial_params.urlencode()