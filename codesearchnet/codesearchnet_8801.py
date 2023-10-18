def _handle_bulk_upload(cls, enterprise_customer, manage_learners_form, request, email_list=None):
        """
        Bulk link users by email.

        Arguments:
            enterprise_customer (EnterpriseCustomer): learners will be linked to this Enterprise Customer instance
            manage_learners_form (ManageLearnersForm): bound ManageLearners form instance
            request (django.http.request.HttpRequest): HTTP Request instance
            email_list (iterable): A list of pre-processed email addresses to handle using the form
        """
        errors = []
        emails = set()
        already_linked_emails = []
        duplicate_emails = []
        csv_file = manage_learners_form.cleaned_data[ManageLearnersForm.Fields.BULK_UPLOAD]
        if email_list:
            parsed_csv = [{ManageLearnersForm.CsvColumns.EMAIL: email} for email in email_list]
        else:
            parsed_csv = parse_csv(csv_file, expected_columns={ManageLearnersForm.CsvColumns.EMAIL})

        try:
            for index, row in enumerate(parsed_csv):
                email = row[ManageLearnersForm.CsvColumns.EMAIL]
                try:
                    already_linked = validate_email_to_link(email, ignore_existing=True)
                except ValidationError as exc:
                    message = _("Error at line {line}: {message}\n").format(line=index + 1, message=exc)
                    errors.append(message)
                else:
                    if already_linked:
                        already_linked_emails.append((email, already_linked.enterprise_customer))
                    elif email in emails:
                        duplicate_emails.append(email)
                    else:
                        emails.add(email)
        except ValidationError as exc:
            errors.append(exc)

        if errors:
            manage_learners_form.add_error(
                ManageLearnersForm.Fields.GENERAL_ERRORS, ValidationMessages.BULK_LINK_FAILED
            )
            for error in errors:
                manage_learners_form.add_error(ManageLearnersForm.Fields.BULK_UPLOAD, error)
            return

        # There were no errors. Now do the actual linking:
        for email in emails:
            EnterpriseCustomerUser.objects.link_user(enterprise_customer, email)

        # Report what happened:
        count = len(emails)
        messages.success(request, ungettext(
            "{count} new learner was added to {enterprise_customer_name}.",
            "{count} new learners were added to {enterprise_customer_name}.",
            count
        ).format(count=count, enterprise_customer_name=enterprise_customer.name))
        this_customer_linked_emails = [
            email for email, customer in already_linked_emails if customer == enterprise_customer
        ]
        other_customer_linked_emails = [
            email for email, __ in already_linked_emails if email not in this_customer_linked_emails
        ]
        if this_customer_linked_emails:
            messages.warning(
                request,
                _(
                    "The following learners were already associated with this Enterprise "
                    "Customer: {list_of_emails}"
                ).format(
                    list_of_emails=", ".join(this_customer_linked_emails)
                )
            )
        if other_customer_linked_emails:
            messages.warning(
                request,
                _(
                    "The following learners are already associated with "
                    "another Enterprise Customer. These learners were not "
                    "added to {enterprise_customer_name}: {list_of_emails}"
                ).format(
                    enterprise_customer_name=enterprise_customer.name,
                    list_of_emails=", ".join(other_customer_linked_emails),
                )
            )
        if duplicate_emails:
            messages.warning(
                request,
                _(
                    "The following duplicate email addresses were not added: "
                    "{list_of_emails}"
                ).format(
                    list_of_emails=", ".join(duplicate_emails)
                )
            )
        # Build a list of all the emails that we can act on further; that is,
        # emails that we either linked to this customer, or that were linked already.
        all_processable_emails = list(emails) + this_customer_linked_emails

        return all_processable_emails