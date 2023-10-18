def get_enterprise_program_enrollment_page(self, request, enterprise_customer, program_details):
        """
        Render Enterprise-specific program enrollment page.
        """
        # Safely make the assumption that we can use the first authoring organization.
        organizations = program_details['authoring_organizations']
        organization = organizations[0] if organizations else {}
        platform_name = get_configuration_value('PLATFORM_NAME', settings.PLATFORM_NAME)
        program_title = program_details['title']
        program_type_details = program_details['type_details']
        program_type = program_type_details['name']

        # Make any modifications for singular/plural-dependent text.
        program_courses = program_details['courses']
        course_count = len(program_courses)
        course_count_text = ungettext(
            '{count} Course',
            '{count} Courses',
            course_count,
        ).format(count=course_count)
        effort_info_text = ungettext_min_max(
            '{} hour per week, per course',
            '{} hours per week, per course',
            _('{}-{} hours per week, per course'),
            program_details.get('min_hours_effort_per_week'),
            program_details.get('max_hours_effort_per_week'),
        )
        length_info_text = ungettext_min_max(
            '{} week per course',
            '{} weeks per course',
            _('{}-{} weeks per course'),
            program_details.get('weeks_to_complete_min'),
            program_details.get('weeks_to_complete_max'),
        )

        # Update some enrollment-related text requirements.
        if program_details['enrolled_in_program']:
            purchase_action = _('Purchase all unenrolled courses')
            item = _('enrollment')
        else:
            purchase_action = _('Pursue the program')
            item = _('program enrollment')

        # Add any DSC warning messages.
        program_data_sharing_consent = get_data_sharing_consent(
            request.user.username,
            enterprise_customer.uuid,
            program_uuid=program_details['uuid'],
        )
        if program_data_sharing_consent.exists and not program_data_sharing_consent.granted:
            messages.add_consent_declined_message(request, enterprise_customer, program_title)

        discount_data = program_details.get('discount_data', {})
        one_click_purchase_eligibility = program_details.get('is_learner_eligible_for_one_click_purchase', False)
        # The following messages shouldn't both appear at the same time, and we prefer the eligibility message.
        if not one_click_purchase_eligibility:
            messages.add_unenrollable_item_message(request, 'program')
        elif discount_data.get('total_incl_tax_excl_discounts') is None:
            messages.add_missing_price_information_message(request, program_title)

        context_data = get_global_context(request, enterprise_customer)
        context_data.update({
            'enrolled_in_course_and_paid_text': _('enrolled'),
            'enrolled_in_course_and_unpaid_text': _('already enrolled, must pay for certificate'),
            'expected_learning_items_text': _("What you'll learn"),
            'expected_learning_items_show_count': 2,
            'corporate_endorsements_text': _('Real Career Impact'),
            'corporate_endorsements_show_count': 1,
            'see_more_text': _('See More'),
            'see_less_text': _('See Less'),
            'confirm_button_text': _('Confirm Program'),
            'summary_header': _('Program Summary'),
            'price_text': _('Price'),
            'length_text': _('Length'),
            'effort_text': _('Effort'),
            'level_text': _('Level'),
            'course_full_description_text': _('About This Course'),
            'staff_text': _('Course Staff'),
            'close_modal_button_text': _('Close'),
            'program_not_eligible_for_one_click_purchase_text': _('Program not eligible for one-click purchase.'),
            'program_type_description_header': _('What is an {platform_name} {program_type}?').format(
                platform_name=platform_name,
                program_type=program_type,
            ),
            'platform_description_header': _('What is {platform_name}?').format(
                platform_name=platform_name
            ),
            'organization_name': organization.get('name'),
            'organization_logo': organization.get('logo_image_url'),
            'organization_text': _('Presented by {organization}').format(organization=organization.get('name')),
            'page_title': _('Confirm your {item}').format(item=item),
            'program_type_logo': program_type_details['logo_image'].get('medium', {}).get('url', ''),
            'program_type': program_type,
            'program_type_description': get_program_type_description(program_type),
            'program_title': program_title,
            'program_subtitle': program_details['subtitle'],
            'program_overview': program_details['overview'],
            'program_price': get_price_text(discount_data.get('total_incl_tax_excl_discounts', 0), request),
            'program_discounted_price': get_price_text(discount_data.get('total_incl_tax', 0), request),
            'is_discounted': discount_data.get('is_discounted', False),
            'courses': program_courses,
            'item_bullet_points': [
                _('Credit- and Certificate-eligible'),
                _('Self-paced; courses can be taken in any order'),
            ],
            'purchase_text': _('{purchase_action} for').format(purchase_action=purchase_action),
            'expected_learning_items': program_details['expected_learning_items'],
            'corporate_endorsements': program_details['corporate_endorsements'],
            'course_count_text': course_count_text,
            'length_info_text': length_info_text,
            'effort_info_text': effort_info_text,
            'is_learner_eligible_for_one_click_purchase': one_click_purchase_eligibility,
        })
        return render(request, 'enterprise/enterprise_program_enrollment_page.html', context=context_data)