def post(self, request):
        """
        POST /enterprise/api/v1/request_codes

        Requires a JSON object of the following format:
        >>> {
        >>>     "email": "bob@alice.com",
        >>>     "enterprise_name": "IBM",
        >>>     "number_of_codes": "50"
        >>> }

        Keys:
        *email*
            Email of the customer who has requested more codes.
        *enterprise_name*
            The name of the enterprise requesting more codes.
        *number_of_codes*
            The number of codes requested.
        """
        try:
            email, enterprise_name, number_of_codes = self.get_required_query_params(request)
        except CodesAPIRequestError as invalid_request:
            return Response({'error': str(invalid_request)}, status=HTTP_400_BAD_REQUEST)

        subject_line = _('Code Management - Request for Codes by {token_enterprise_name}').format(
            token_enterprise_name=enterprise_name
        )
        msg_with_codes = _('{token_email} from {token_enterprise_name} has requested {token_number_codes} additional '
                           'codes. Please reach out to them.').format(
                               token_email=email,
                               token_enterprise_name=enterprise_name,
                               token_number_codes=number_of_codes)
        msg_without_codes = _('{token_email} from {token_enterprise_name} has requested additional codes.'
                              ' Please reach out to them.').format(
                                  token_email=email,
                                  token_enterprise_name=enterprise_name)
        app_config = apps.get_app_config("enterprise")
        from_email_address = app_config.customer_success_email
        cs_email = app_config.customer_success_email
        data = {
            self.REQUIRED_PARAM_EMAIL: email,
            self.REQUIRED_PARAM_ENTERPRISE_NAME: enterprise_name,
            self.OPTIONAL_PARAM_NUMBER_OF_CODES: number_of_codes,
        }
        try:
            mail.send_mail(
                subject_line,
                msg_with_codes if number_of_codes else msg_without_codes,
                from_email_address,
                [cs_email],
                fail_silently=False
            )
            return Response(data, status=HTTP_200_OK)
        except SMTPException:
            error_message = _(
                '[Enterprise API] Failure in sending e-mail to {token_cs_email} for {token_email}'
                ' from {token_enterprise_name}'
            ).format(
                token_cs_email=cs_email,
                token_email=email,
                token_enterprise_name=enterprise_name
            )
            LOGGER.error(error_message)
            return Response(
                {'error': str('Request codes email could not be sent')},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )