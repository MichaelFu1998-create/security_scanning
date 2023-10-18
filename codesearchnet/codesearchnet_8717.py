def get_context_from_db(self, consent_page, platform_name, item, context):
        """
        Make set of variables(populated from db) that will be used in data sharing consent page.
        """
        enterprise_customer = consent_page.enterprise_customer
        course_title = context.get('course_title', None)
        course_start_date = context.get('course_start_date', None)
        context_data = {
            'text_override_available': True,
            'page_title': consent_page.page_title,
            'left_sidebar_text': consent_page.left_sidebar_text.format(
                enterprise_customer_name=enterprise_customer.name,
                platform_name=platform_name,
                item=item,
                course_title=course_title,
                course_start_date=course_start_date,
            ),
            'top_paragraph': consent_page.top_paragraph.format(
                enterprise_customer_name=enterprise_customer.name,
                platform_name=platform_name,
                item=item,
                course_title=course_title,
                course_start_date=course_start_date,
            ),
            'agreement_text': consent_page.agreement_text.format(
                enterprise_customer_name=enterprise_customer.name,
                platform_name=platform_name,
                item=item,
                course_title=course_title,
                course_start_date=course_start_date,
            ),
            'continue_text': consent_page.continue_text,
            'abort_text': consent_page.abort_text,
            'policy_dropdown_header': consent_page.policy_dropdown_header,
            'policy_paragraph': consent_page.policy_paragraph.format(
                enterprise_customer_name=enterprise_customer.name,
                platform_name=platform_name,
                item=item,
                course_title=course_title,
                course_start_date=course_start_date,
            ),
            'confirmation_modal_header': consent_page.confirmation_modal_header.format(
                enterprise_customer_name=enterprise_customer.name,
                platform_name=platform_name,
                item=item,
                course_title=course_title,
                course_start_date=course_start_date,
            ),
            'confirmation_alert_prompt': consent_page.confirmation_modal_text.format(
                enterprise_customer_name=enterprise_customer.name,
                platform_name=platform_name,
                item=item,
                course_title=course_title,
                course_start_date=course_start_date,
            ),
            'confirmation_modal_affirm_decline_text': consent_page.modal_affirm_decline_text,
            'confirmation_modal_abort_decline_text': consent_page.modal_abort_decline_text,
        }
        return context_data