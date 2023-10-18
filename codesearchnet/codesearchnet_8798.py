def get_enterprise_customer_user_queryset(self, request, search_keyword, customer_uuid, page_size=PAGE_SIZE):
        """
        Get the list of EnterpriseCustomerUsers we want to render.

        Arguments:
            request (HttpRequest): HTTP Request instance.
            search_keyword (str): The keyword to search for in users' email addresses and usernames.
            customer_uuid (str): A unique identifier to filter down to only users linked to a
            particular EnterpriseCustomer.
            page_size (int): Number of learners displayed in each paginated set.
        """
        page = request.GET.get('page', 1)
        learners = EnterpriseCustomerUser.objects.filter(enterprise_customer__uuid=customer_uuid)
        user_ids = learners.values_list('user_id', flat=True)
        matching_users = User.objects.filter(pk__in=user_ids)
        if search_keyword is not None:
            matching_users = matching_users.filter(
                Q(email__icontains=search_keyword) | Q(username__icontains=search_keyword)
            )
        matching_user_ids = matching_users.values_list('pk', flat=True)
        learners = learners.filter(user_id__in=matching_user_ids)
        return paginated_list(learners, page, page_size)