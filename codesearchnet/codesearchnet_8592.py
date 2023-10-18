def get_groups(self, obj):
        """
        Return the enterprise related django groups that this user is a part of.
        """
        if obj.user:
            return [group.name for group in obj.user.groups.filter(name__in=ENTERPRISE_PERMISSION_GROUPS)]
        return []