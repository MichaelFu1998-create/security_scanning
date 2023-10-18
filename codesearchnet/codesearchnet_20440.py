def stream(cls, response, sequence):
        """
        Helper method used in conjunction with the view handler to
        stream responses to the client.
        """
        # Construct the iterator and run the sequence once in order
        # to capture any headers and status codes set.
        iterator = iter(sequence)
        data = {'chunk': next(iterator)}
        response.streaming = True

        def streamer():
            # Iterate through the iterator and yield its content
            while True:
                if response.asynchronous:
                    # Yield our current chunk.
                    yield data['chunk']

                else:
                    # Write the chunk to the response
                    response.send(data['chunk'])

                    # Yield its body
                    yield response.body

                    # Unset the body.
                    response.body = None

                try:
                    # Get the next chunk.
                    data['chunk'] = next(iterator)

                except StopIteration:
                    # Get out of the loop.
                    break

            if not response.asynchronous:
                # Close the response.
                response.close()

        # Return the streaming function.
        return streamer()