def set_final_prices(self, modes, request):
        """
        Set the final discounted price on each premium mode.
        """
        result = []
        for mode in modes:
            if mode['premium']:
                mode['final_price'] = EcommerceApiClient(request.user).get_course_final_price(
                    mode=mode,
                    enterprise_catalog_uuid=request.GET.get(
                        'catalog'
                    ) if request.method == 'GET' else None,
                )
            result.append(mode)
        return result