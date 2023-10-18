def deref(self, data):
        """AWS doesn't quite have Swagger 2.0 validation right and will fail
        on some refs. So, we need to convert to deref before
        upload."""

        # We have to make a deepcopy here to create a proper JSON
        # compatible object, otherwise `json.dumps` fails when it
        # hits jsonref.JsonRef objects.
        deref = copy.deepcopy(jsonref.JsonRef.replace_refs(data))

        # Write out JSON version because we might want this.
        self.write_template(deref, filename='swagger.json')

        return deref