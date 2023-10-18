def get_base_details(self, request, enterprise_uuid, course_run_id):
        """
        Retrieve fundamental details used by both POST and GET versions of this view.

        Specifically, take an EnterpriseCustomer UUID and a course run ID, and transform those
        into an actual EnterpriseCustomer, a set of details about the course, and a list
        of the available course modes for that course run.
        """
        enterprise_customer = get_enterprise_customer_or_404(enterprise_uuid)

        # If the catalog query parameter was provided, we need to scope
        # this request to the specified EnterpriseCustomerCatalog.
        enterprise_catalog_uuid = request.GET.get('catalog')
        enterprise_catalog = None
        if enterprise_catalog_uuid:
            try:
                enterprise_catalog_uuid = UUID(enterprise_catalog_uuid)
                enterprise_catalog = enterprise_customer.enterprise_customer_catalogs.get(
                    uuid=enterprise_catalog_uuid
                )
            except (ValueError, EnterpriseCustomerCatalog.DoesNotExist):
                LOGGER.warning(
                    'EnterpriseCustomerCatalog [{enterprise_catalog_uuid}] does not exist'.format(
                        enterprise_catalog_uuid=enterprise_catalog_uuid,
                    )
                )
                messages.add_generic_info_message_for_error(request)

        course = None
        course_run = None
        course_modes = []
        if enterprise_catalog:
            course, course_run = enterprise_catalog.get_course_and_course_run(course_run_id)
        else:
            try:
                course, course_run = CourseCatalogApiServiceClient(
                    enterprise_customer.site
                ).get_course_and_course_run(course_run_id)
            except ImproperlyConfigured:
                LOGGER.warning('CourseCatalogApiServiceClient is improperly configured.')
                messages.add_generic_info_message_for_error(request)
                return enterprise_customer, course, course_run, course_modes

        if not course or not course_run:
            course_id = course['key'] if course else "Not Found"
            course_title = course['title'] if course else "Not Found"
            course_run_title = course_run['title'] if course_run else "Not Found"
            enterprise_catalog_title = enterprise_catalog.title if enterprise_catalog else "Not Found"
            # The specified course either does not exist in the specified
            # EnterpriseCustomerCatalog, or does not exist at all in the
            # discovery service.
            LOGGER.warning(
                'Failed to fetch details for course "{course_title}" [{course_id}] '
                'or course run "{course_run_title}" [{course_run_id}] '
                'for enterprise "{enterprise_name}" [{enterprise_uuid}] '
                'with catalog "{enterprise_catalog_title}" [{enterprise_catalog_uuid}]'.format(
                    course_title=course_title,
                    course_id=course_id,
                    course_run_title=course_run_title,
                    course_run_id=course_run_id,
                    enterprise_name=enterprise_customer.name,
                    enterprise_uuid=enterprise_customer.uuid,
                    enterprise_catalog_title=enterprise_catalog_title,
                    enterprise_catalog_uuid=enterprise_catalog_uuid,
                )
            )
            messages.add_generic_info_message_for_error(request)
            return enterprise_customer, course, course_run, course_modes

        if enterprise_catalog_uuid and not enterprise_catalog:
            # A catalog query parameter was given, but the specified
            # EnterpriseCustomerCatalog does not exist, so just return and
            # display the generic error message.
            return enterprise_customer, course, course_run, course_modes

        modes = self.get_available_course_modes(request, course_run_id, enterprise_catalog)
        audit_modes = getattr(
            settings,
            'ENTERPRISE_COURSE_ENROLLMENT_AUDIT_MODES',
            ['audit', 'honor']
        )

        for mode in modes:
            if mode['min_price']:
                price_text = get_price_text(mode['min_price'], request)
            else:
                price_text = _('FREE')
            if mode['slug'] in audit_modes:
                description = _('Not eligible for a certificate.')
            else:
                description = _('Earn a verified certificate!')
            course_modes.append({
                'mode': mode['slug'],
                'min_price': mode['min_price'],
                'sku': mode['sku'],
                'title': mode['name'],
                'original_price': price_text,
                'final_price': price_text,
                'description': description,
                'premium': mode['slug'] not in audit_modes
            })

        return enterprise_customer, course, course_run, course_modes