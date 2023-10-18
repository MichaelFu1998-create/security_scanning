def parse_filter(self, filters):
        """ This method process the filters """
        for filter_type in filters:
            if filter_type == 'or' or filter_type == 'and':
                conditions = []
                for field in filters[filter_type]:
                    if self.is_field_allowed(field):
                        conditions.append(self.create_query(self.parse_field(field, filters[filter_type][field])))
                if filter_type == 'or':
                    self.model_query = self.model_query.filter(or_(*conditions))
                elif filter_type == 'and':
                    self.model_query = self.model_query.filter(and_(*conditions))
            else:
                if self.is_field_allowed(filter_type):
                    conditions = self.create_query(self.parse_field(filter_type, filters[filter_type]))
                    self.model_query = self.model_query.filter(conditions)
        return self.model_query