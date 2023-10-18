def make_response(self, data=None):
        """Fills the response object from the passed data."""
        if data is not None:
            # Prepare the data for transmission.
            data = self.prepare(data)

            # Encode the data using a desired encoder.
            self.response.write(data, serialize=True)