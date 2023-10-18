def add_safety_checks(meta, members):
        """
        Iterate through each member of the class being created and add a 
        safety check to every method that isn't marked as read-only.
        """
        for member_name, member_value in members.items():
            members[member_name] = meta.add_safety_check(
                    member_name, member_value)