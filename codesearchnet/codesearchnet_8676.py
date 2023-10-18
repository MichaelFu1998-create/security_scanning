def enterprise_customer_uuid(self):
        """Get the enterprise customer uuid linked to the user."""
        try:
            enterprise_user = EnterpriseCustomerUser.objects.get(user_id=self.user.id)
        except ObjectDoesNotExist:
            LOGGER.warning(
                'User {} has a {} assignment but is not linked to an enterprise!'.format(
                    self.__class__,
                    self.user.id
                ))
            return None
        except MultipleObjectsReturned:
            LOGGER.warning(
                'User {} is linked to multiple enterprises, which is not yet supported!'.format(self.user.id)
            )
            return None

        return str(enterprise_user.enterprise_customer.uuid)