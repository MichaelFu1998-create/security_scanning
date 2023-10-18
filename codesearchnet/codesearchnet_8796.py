def post(self, request, enterprise_customer_uuid):
        """
        Handle POST request - handle form submissions.

        Arguments:
            request (django.http.request.HttpRequest): Request instance
            enterprise_customer_uuid (str): Enterprise Customer UUID
        """
        transmit_courses_metadata_form = TransmitEnterpriseCoursesForm(request.POST)

        # check that form data is well-formed
        if transmit_courses_metadata_form.is_valid():
            channel_worker_username = transmit_courses_metadata_form.cleaned_data['channel_worker_username']

            # call `transmit_content_metadata` management command to trigger
            # transmission of enterprise courses metadata
            call_command(
                'transmit_content_metadata',
                '--catalog_user', channel_worker_username,
                enterprise_customer=enterprise_customer_uuid
            )

            # Redirect to GET
            return HttpResponseRedirect('')

        context = self._build_context(request, enterprise_customer_uuid)
        context.update({self.ContextParameters.TRANSMIT_COURSES_METADATA_FORM: transmit_courses_metadata_form})
        return render(request, self.template, context)