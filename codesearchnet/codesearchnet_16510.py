def sorted_components(self):
        """iterator that returns (component,object) in id order"""
        for component, object in \
                sorted(self.components.items(),
                       key=lambda comp_obj: comp_obj[1].id):
            yield component, object