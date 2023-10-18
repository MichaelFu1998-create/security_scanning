def serialize(self, data=None):
        """
        Transforms the object into an acceptable format for transmission.

        @throws ValueError
            To indicate this serializer does not support the encoding of the
            specified object.
        """
        if data is not None and self.response is not None:
            # Set the content type.
            self.response['Content-Type'] = self.media_types[0]

            # Write the encoded and prepared data to the response.
            self.response.write(data)

        # Return the serialized data.
        # This has normally been transformed by a base class.
        return data