def create(cls, name=None, description='', privacy_policy=None,
               subscription_policy=None, is_managed=False, admins=None):
        """Create a new group.

        :param name: Name of group. Required and must be unique.
        :param description: Description of group. Default: ``''``
        :param privacy_policy: PrivacyPolicy
        :param subscription_policy: SubscriptionPolicy
        :param admins: list of user and/or group objects. Default: ``[]``
        :returns: Newly created group
        :raises: IntegrityError: if group with given name already exists
        """
        assert name
        assert privacy_policy is None or PrivacyPolicy.validate(privacy_policy)
        assert subscription_policy is None or \
            SubscriptionPolicy.validate(subscription_policy)
        assert admins is None or isinstance(admins, list)

        with db.session.begin_nested():
            obj = cls(
                name=name,
                description=description,
                privacy_policy=privacy_policy,
                subscription_policy=subscription_policy,
                is_managed=is_managed,
            )
            db.session.add(obj)

            for a in admins or []:
                db.session.add(GroupAdmin(
                    group=obj, admin_id=a.get_id(),
                    admin_type=resolve_admin_type(a)))

        return obj