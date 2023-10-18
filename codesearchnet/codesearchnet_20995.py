def add_safety_check(member_name, member_value):
        """
        If the given member is a method that is public (i.e. doesn't start with 
        an underscore) and hasn't been marked as read-only, replace it with a 
        version that will check to make sure the world is locked.  This ensures 
        that methods that alter the token are only called from update methods 
        or messages.
        """
        import functools
        from types import FunctionType

        # Bail if the given member is read-only, private, or not a method.

        is_method = isinstance(member_value, FunctionType)
        is_read_only = hasattr(member_value, '_kxg_read_only')
        is_private = member_name.startswith('_')

        if not is_method or is_read_only or is_private:
            return member_value

        def safety_checked_method(self, *args, **kwargs):
            """
            Make sure that the token the world is locked before a non-read-only 
            method is called.
            """
            # Because these checks are pretty magical, I want to be really 
            # careful to avoid raising any exceptions other than the check 
            # itself (which comes with a very clear error message).  Here, that 
            # means using getattr() to make sure the world attribute actually 
            # exists.  For example, there's nothing wrong with the following 
            # code, but it does call a safety-checked method before the world 
            # attribute is defined:
            #
            # class MyToken(kxg.Token):
            #     def __init__(self):
            #         self.init_helper()
            #         super().__init__()

            world = getattr(self, 'world', None)
            if world and world.is_locked():
                nonlocal member_name
                raise ApiUsageError("""\
                        attempted unsafe invocation of 
                        {self.__class__.__name__}.{member_name}().

                        This error brings attention to situations that might 
                        cause synchronization issues in multiplayer games.  The 
                        {member_name}() method is not marked as read-only, but 
                        it was invoked from outside the context of a message.  
                        This means that if {member_name}() makes any changes to 
                        the world, those changes will not be propagated.  If 
                        {member_name}() is actually read-only, label it with 
                        the @kxg.read_only decorator.""")

            # After making that check, call the method as usual.

            return member_value(self, *args, **kwargs)

        # Preserve any "forum observer" decorations that have been placed on 
        # the method and restore the method's original name and module strings, 
        # to make inspection and debugging a little easier.

        functools.update_wrapper(
                safety_checked_method, member_value,
                assigned=functools.WRAPPER_ASSIGNMENTS + (
                    '_kxg_subscribe_to_message',
                    '_kxg_subscribe_to_sync_response',
                    '_kxg_subscribe_to_undo_response',
                )
        )
        return safety_checked_method