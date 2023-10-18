def get(self, request, enterprise_customer_uuid):
        """
        Handle GET request - render "Transmit courses metadata" form.

        Arguments:
            request (django.http.request.HttpRequest): Request instance
            enterprise_customer_uuid (str): Enterprise Customer UUID

        Returns:
            django.http.response.HttpResponse: HttpResponse
        """
        context = self._build_context(request, enterprise_customer_uuid)
        transmit_courses_metadata_form = TransmitEnterpriseCoursesForm()
        context.update({self.ContextParameters.TRANSMIT_COURSES_METADATA_FORM: transmit_courses_metadata_form})

        return render(request, self.template, context)