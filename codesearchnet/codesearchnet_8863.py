def ecommerce_coupon_url(self, instance):
        """
        Instance is EnterpriseCustomer. Return e-commerce coupon urls.
        """
        if not instance.entitlement_id:
            return "N/A"

        return format_html(
            '<a href="{base_url}/coupons/{id}" target="_blank">View coupon "{id}" details</a>',
            base_url=settings.ECOMMERCE_PUBLIC_URL_ROOT, id=instance.entitlement_id
        )