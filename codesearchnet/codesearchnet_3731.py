def configure_model(self, attrs, field_name):
        '''
        Hook for ResourceMeta class to call when initializing model class.
        Saves fields obtained from resource class backlinks
        '''
        self.relationship = field_name
        self._set_method_names(relationship=field_name)
        if self.res_name is None:
            self.res_name = grammar.singularize(attrs.get('endpoint', 'unknown').strip('/'))