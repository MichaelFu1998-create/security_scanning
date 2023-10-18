def post(self, request, enterprise_uuid, program_uuid):
        """
        Process a submitted track selection form for the enterprise.
        """
        verify_edx_resources()

        # Create a link between the user and the enterprise customer if it does not already exist.
        enterprise_customer = get_enterprise_customer_or_404(enterprise_uuid)
        with transaction.atomic():
            enterprise_customer_user, __ = EnterpriseCustomerUser.objects.get_or_create(
                enterprise_customer=enterprise_customer,
                user_id=request.user.id
            )
            enterprise_customer_user.update_session(request)

        context_data = get_global_context(request, enterprise_customer)
        program_details, error_code = self.get_program_details(request, program_uuid, enterprise_customer)
        if error_code:
            return render(
                request,
                ENTERPRISE_GENERAL_ERROR_PAGE,
                context=context_data,
                status=404,
            )
        if program_details['certificate_eligible_for_program']:
            # The user is already enrolled in the program, so redirect to the program's dashboard.
            return redirect(LMS_PROGRAMS_DASHBOARD_URL.format(uuid=program_uuid))

        basket_page = '{basket_url}?{params}'.format(
            basket_url=BASKET_URL,
            params=urlencode(
                [tuple(['sku', sku]) for sku in program_details['skus']] +
                [tuple(['bundle', program_uuid])]
            )
        )
        if get_data_sharing_consent(
                enterprise_customer_user.username,
                enterprise_customer.uuid,
                program_uuid=program_uuid,
        ).consent_required():
            return redirect(
                '{grant_data_sharing_url}?{params}'.format(
                    grant_data_sharing_url=reverse('grant_data_sharing_permissions'),
                    params=urlencode(
                        {
                            'next': basket_page,
                            'failure_url': reverse(
                                'enterprise_program_enrollment_page',
                                args=[enterprise_customer.uuid, program_uuid]
                            ),
                            'enterprise_customer_uuid': enterprise_customer.uuid,
                            'program_uuid': program_uuid,
                        }
                    )
                )
            )

        return redirect(basket_page)