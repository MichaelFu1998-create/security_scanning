def can_diff(msg_a, msg_b):
        """
        Check if two thrift messages are diff ready.

        Returns a tuple of (boolean, reason_string), i.e. (False, reason_string)
        if the messages can not be diffed along with the reason and
        (True, None) for the opposite case
        """
        if msg_a.method != msg_b.method:
            return False, 'method name of messages do not match'
        if len(msg_a.args) != len(msg_b.args) \
                or not msg_a.args.is_isomorphic_to(msg_b.args):
            return False, 'argument signature of methods do not match'
        return True, None