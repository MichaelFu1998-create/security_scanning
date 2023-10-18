def post(self, request):
        """
        Save the provided data using the class' serializer.

        Args:
            request:
                The request being made.

        Returns:
            An ``APIResponse`` instance. If the request was successful
            the response will have a 200 status code and contain the
            serializer's data. Otherwise a 400 status code and the
            request's errors will be returned.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)