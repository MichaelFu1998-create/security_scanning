def cmd(admin_only=False, acl='*', aliases=None, while_ignored=False, *args, **kwargs):
    """
    Decorator to mark plugin functions as commands in the form of !<cmd_name>

    * admin_only - indicates only users in bot_admin are allowed to execute (only used if AuthManager is loaded)
    * acl - indicates which ACL to perform permission checks against (only used if AuthManager is loaded)
    * aliases - register function with additional commands (i.e. !alias1, !alias2, etc)
    * while_ignored - allows a command to be run, even if channel has been !sleep
    """
    def wrapper(func):
        func.is_cmd = True
        func.is_subcmd = len(func.__name__.split('_')) > 1
        func.cmd_name = func.__name__.replace('_', ' ')
        func.admin_only = admin_only
        func.acl = acl
        func.aliases = aliases
        func.while_ignored = while_ignored
        return func
    return wrapper