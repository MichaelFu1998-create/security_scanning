def handle_package_literal_optional(self, package, package_node, predicate, field):
        """
        Check if optional field is set.
        If so it adds the triple (package_node, predicate, $) to the graph.
        Where $ is a literal or special value term of the value of the field.
        """
        if package.has_optional_field(field):
            value = getattr(package, field, None)
            value_node = self.to_special_value(value)
            triple = (package_node, predicate, value_node)
            self.graph.add(triple)