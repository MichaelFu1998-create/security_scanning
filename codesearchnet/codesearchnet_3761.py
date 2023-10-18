def configure_display(self, data, kwargs=None, write=False):
        """Populates columns and sets display attribute as needed.
        Operates on data."""
        if settings.format != 'human':
            return  # This is only used for human format
        if write:
            obj, obj_type, res, res_type = self.obj_res(kwargs)
            data['type'] = kwargs['type']
            data[obj_type] = obj
            data[res_type] = res
            self.set_display_columns(
                set_false=['team' if obj_type == 'user' else 'user'],
                set_true=['target_team' if res_type == 'team' else res_type])
        else:
            self.set_display_columns(
                set_false=['user', 'team'],
                set_true=['resource_name', 'resource_type'])
            if 'results' in data:
                for i in range(len(data['results'])):
                    self.populate_resource_columns(data['results'][i])
            else:
                self.populate_resource_columns(data)