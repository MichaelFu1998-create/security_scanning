def get_enterprise_course_enrollment_page(
            self,
            request,
            enterprise_customer,
            course,
            course_run,
            course_modes,
            enterprise_course_enrollment,
            data_sharing_consent
    ):
        """
        Render enterprise-specific course track selection page.
        """
        context_data = get_global_context(request, enterprise_customer)
        enterprise_catalog_uuid = request.GET.get(
            'catalog'
        ) if request.method == 'GET' else None
        html_template_for_rendering = ENTERPRISE_GENERAL_ERROR_PAGE
        if course and course_run:
            course_enrollable = True
            course_start_date = ''
            course_in_future = False
            organization_name = ''
            organization_logo = ''
            expected_learning_items = course['expected_learning_items']
            # Parse organization name and logo.
            if course['owners']:
                # The owners key contains the organizations associated with the course.
                # We pick the first one in the list here to meet UX requirements.
                organization = course['owners'][0]
                organization_name = organization['name']
                organization_logo = organization['logo_image_url']

            course_title = course_run['title']
            course_short_description = course_run['short_description'] or ''
            course_full_description = clean_html_for_template_rendering(course_run['full_description'] or '')
            course_pacing = self.PACING_FORMAT.get(course_run['pacing_type'], '')
            if course_run['start']:
                course_start_date = parse(course_run['start']).strftime('%B %d, %Y')
                now = datetime.datetime.now(pytz.UTC)
                course_in_future = parse(course_run['start']) > now

            course_level_type = course_run.get('level_type', '')
            staff = course_run['staff']
            # Format the course effort string using the min/max effort fields for the course run.
            course_effort = ungettext_min_max(
                '{} hour per week',
                '{} hours per week',
                '{}-{} hours per week',
                course_run['min_effort'] or None,
                course_run['max_effort'] or None,
            ) or ''

            # Parse course run image.
            course_run_image = course_run['image'] or {}
            course_image_uri = course_run_image.get('src', '')

            # Retrieve the enterprise-discounted price from ecommerce.
            course_modes = self.set_final_prices(course_modes, request)
            premium_modes = [mode for mode in course_modes if mode['premium']]

            # Filter audit course modes.
            course_modes = filter_audit_course_modes(enterprise_customer, course_modes)

            # Allows automatic assignment to a cohort upon enrollment.
            cohort = request.GET.get('cohort')
            # Add a message to the message display queue if the learner
            # has gone through the data sharing consent flow and declined
            # to give data sharing consent.
            if enterprise_course_enrollment and not data_sharing_consent.granted:
                messages.add_consent_declined_message(request, enterprise_customer, course_run.get('title', ''))

            if not is_course_run_enrollable(course_run):
                messages.add_unenrollable_item_message(request, 'course')
                course_enrollable = False
            context_data.update({
                'course_enrollable': course_enrollable,
                'course_title': course_title,
                'course_short_description': course_short_description,
                'course_pacing': course_pacing,
                'course_start_date': course_start_date,
                'course_in_future': course_in_future,
                'course_image_uri': course_image_uri,
                'course_modes': course_modes,
                'course_effort': course_effort,
                'course_full_description': course_full_description,
                'cohort': cohort,
                'organization_logo': organization_logo,
                'organization_name': organization_name,
                'course_level_type': course_level_type,
                'premium_modes': premium_modes,
                'expected_learning_items': expected_learning_items,
                'catalog': enterprise_catalog_uuid,
                'staff': staff,
                'discount_text': _('Discount provided by {strong_start}{enterprise_customer_name}{strong_end}').format(
                    enterprise_customer_name=enterprise_customer.name,
                    strong_start='<strong>',
                    strong_end='</strong>',
                ),
                'hide_course_original_price': enterprise_customer.hide_course_original_price
            })
            html_template_for_rendering = 'enterprise/enterprise_course_enrollment_page.html'

        context_data.update({
            'page_title': _('Confirm your course'),
            'confirmation_text': _('Confirm your course'),
            'starts_at_text': _('Starts'),
            'view_course_details_text': _('View Course Details'),
            'select_mode_text': _('Please select one:'),
            'price_text': _('Price'),
            'continue_link_text': _('Continue'),
            'level_text': _('Level'),
            'effort_text': _('Effort'),
            'close_modal_button_text': _('Close'),
            'expected_learning_items_text': _("What you'll learn"),
            'course_full_description_text': _('About This Course'),
            'staff_text': _('Course Staff'),
        })
        return render(request, html_template_for_rendering, context=context_data)