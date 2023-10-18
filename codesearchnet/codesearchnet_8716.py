def get_default_context(self, enterprise_customer, platform_name):
        """
        Get the set of variables that will populate the template by default.
        """
        context_data = {
            'page_title': _('Data sharing consent required'),
            'consent_message_header': _('Consent to share your data'),
            'requested_permissions_header': _(
                'Per the {start_link}Data Sharing Policy{end_link}, '
                '{bold_start}{enterprise_customer_name}{bold_end} would like to know about:'
            ).format(
                enterprise_customer_name=enterprise_customer.name,
                bold_start='<b>',
                bold_end='</b>',
                start_link='<a href="#consent-policy-dropdown-bar" '
                           'class="policy-dropdown-link background-input" id="policy-dropdown-link">',
                end_link='</a>',
            ),
            'agreement_text': _(
                'I agree to allow {platform_name} to share data about my enrollment, completion and performance in all '
                '{platform_name} courses and programs where my enrollment is sponsored by {enterprise_customer_name}.'
            ).format(
                enterprise_customer_name=enterprise_customer.name,
                platform_name=platform_name,
            ),
            'continue_text': _('Yes, continue'),
            'abort_text': _('No, take me back.'),
            'policy_dropdown_header': _('Data Sharing Policy'),
            'sharable_items_header': _(
                'Enrollment, completion, and performance data that may be shared with {enterprise_customer_name} '
                '(or its designee) for these courses and programs are limited to the following:'
            ).format(
                enterprise_customer_name=enterprise_customer.name
            ),
            'sharable_items': [
                _(
                    'My email address for my {platform_name} account, '
                    'and the date when I created my {platform_name} account'
                ).format(
                    platform_name=platform_name
                ),
                _(
                    'My {platform_name} ID, and if I log in via single sign-on, '
                    'my {enterprise_customer_name} SSO user-ID'
                ).format(
                    platform_name=platform_name,
                    enterprise_customer_name=enterprise_customer.name,
                ),
                _('My {platform_name} username').format(platform_name=platform_name),
                _('My country or region of residence'),
                _(
                    'What courses and/or programs I\'ve enrolled in or unenrolled from, what track I '
                    'enrolled in (audit or verified) and the date when I enrolled in each course or program'
                ),
                _(
                    'Information about each course or program I\'ve enrolled in, '
                    'including its duration and level of effort required'
                ),
                _(
                    'Whether I completed specific parts of each course or program (for example, whether '
                    'I watched a given video or completed a given homework assignment)'
                ),
                _(
                    'My overall percentage completion of each course or program on a periodic basis, '
                    'including the total time spent in each course or program and the date when I last '
                    'logged in to each course or program'
                ),
                _('My performance in each course or program'),
                _('My final grade in each course or program, and the date when I completed each course or program'),
                _('Whether I received a certificate in each course or program'),
            ],
            'sharable_items_footer': _(
                'My permission applies only to data from courses or programs that are sponsored by '
                '{enterprise_customer_name}, and not to data from any {platform_name} courses or programs that '
                'I take on my own. I understand that I may withdraw my permission only by fully unenrolling '
                'from any courses or programs that are sponsored by {enterprise_customer_name}.'
            ).format(
                enterprise_customer_name=enterprise_customer.name,
                platform_name=platform_name,
            ),
            'sharable_items_note_header': _('Please note'),
            'sharable_items_notes': [
                _('If you decline to consent, that fact may be shared with {enterprise_customer_name}.').format(
                    enterprise_customer_name=enterprise_customer.name
                ),
            ],
            'confirmation_modal_header': _('Are you aware...'),
            'confirmation_modal_affirm_decline_text': _('I decline'),
            'confirmation_modal_abort_decline_text': _('View the data sharing policy'),
            'policy_link_template': _('View the {start_link}data sharing policy{end_link}.').format(
                start_link='<a href="#consent-policy-dropdown-bar" class="policy-dropdown-link background-input" '
                           'id="policy-dropdown-link">',
                end_link='</a>',
            ),
            'policy_return_link_text': _('Return to Top'),
        }
        return context_data