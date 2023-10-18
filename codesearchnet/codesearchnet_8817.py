def from_children(cls, program_uuid, *children):
        """
        Build a ProxyDataSharingConsent using the details of the received consent records.
        """
        if not children or any(child is None for child in children):
            return None
        granted = all((child.granted for child in children))
        exists = any((child.exists for child in children))
        usernames = set([child.username for child in children])
        enterprises = set([child.enterprise_customer for child in children])
        if not len(usernames) == len(enterprises) == 1:
            raise InvalidProxyConsent(
                'Children used to create a bulk proxy consent object must '
                'share a single common username and EnterpriseCustomer.'
            )
        username = children[0].username
        enterprise_customer = children[0].enterprise_customer
        return cls(
            enterprise_customer=enterprise_customer,
            username=username,
            program_uuid=program_uuid,
            exists=exists,
            granted=granted,
            child_consents=children
        )