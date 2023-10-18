def post(self, request, customer_uuid):
        """
        Handle POST request - handle form submissions.

        Arguments:
            request (django.http.request.HttpRequest): Request instance
            customer_uuid (str): Enterprise Customer UUID

        Returns:
            django.http.response.HttpResponse: HttpResponse
        """
        enterprise_customer = EnterpriseCustomer.objects.get(uuid=customer_uuid)  # pylint: disable=no-member
        manage_learners_form = ManageLearnersForm(
            request.POST,
            request.FILES,
            user=request.user,
            enterprise_customer=enterprise_customer
        )

        # initial form validation - check that form data is well-formed
        if manage_learners_form.is_valid():
            email_field_as_bulk_input = split_usernames_and_emails(
                manage_learners_form.cleaned_data[ManageLearnersForm.Fields.EMAIL_OR_USERNAME]
            )
            is_bulk_entry = len(email_field_as_bulk_input) > 1
            # The form is valid. Call the appropriate helper depending on the mode:
            mode = manage_learners_form.cleaned_data[ManageLearnersForm.Fields.MODE]
            if mode == ManageLearnersForm.Modes.MODE_SINGULAR and not is_bulk_entry:
                linked_learners = self._handle_singular(enterprise_customer, manage_learners_form)
            elif mode == ManageLearnersForm.Modes.MODE_SINGULAR:
                linked_learners = self._handle_bulk_upload(
                    enterprise_customer,
                    manage_learners_form,
                    request,
                    email_list=email_field_as_bulk_input
                )
            else:
                linked_learners = self._handle_bulk_upload(enterprise_customer, manage_learners_form, request)

        # _handle_form might add form errors, so we check if it is still valid
        if manage_learners_form.is_valid():
            course_details = manage_learners_form.cleaned_data.get(ManageLearnersForm.Fields.COURSE)
            program_details = manage_learners_form.cleaned_data.get(ManageLearnersForm.Fields.PROGRAM)

            notification_type = manage_learners_form.cleaned_data.get(ManageLearnersForm.Fields.NOTIFY)
            notify = notification_type == ManageLearnersForm.NotificationTypes.BY_EMAIL

            course_id = None
            if course_details:
                course_id = course_details['course_id']

            if course_id or program_details:
                course_mode = manage_learners_form.cleaned_data[ManageLearnersForm.Fields.COURSE_MODE]
                self._enroll_users(
                    request=request,
                    enterprise_customer=enterprise_customer,
                    emails=linked_learners,
                    mode=course_mode,
                    course_id=course_id,
                    program_details=program_details,
                    notify=notify,
                )

            # Redirect to GET if everything went smooth.
            manage_learners_url = reverse("admin:" + UrlNames.MANAGE_LEARNERS, args=(customer_uuid,))
            search_keyword = self.get_search_keyword(request)
            if search_keyword:
                manage_learners_url = manage_learners_url + "?q=" + search_keyword
            return HttpResponseRedirect(manage_learners_url)

        # if something went wrong - display bound form on the page
        context = self._build_context(request, customer_uuid)
        context.update({self.ContextParameters.MANAGE_LEARNERS_FORM: manage_learners_form})
        return render(request, self.template, context)