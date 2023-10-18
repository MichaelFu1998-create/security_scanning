def acl_show(self, msg, args):
        """Show current allow and deny blocks for the given acl."""
        name = args[0] if len(args) > 0 else None
        if name is None:
            return "%s: The following ACLs are defined: %s" % (msg.user, ', '.join(self._acl.keys()))

        if name not in self._acl:
            return "Sorry, couldn't find an acl named '%s'" % name

        return '\n'.join([
            "%s: ACL '%s' is defined as follows:" % (msg.user, name),
            "allow: %s" % ', '.join(self._acl[name]['allow']),
            "deny: %s" % ', '.join(self._acl[name]['deny'])
        ])