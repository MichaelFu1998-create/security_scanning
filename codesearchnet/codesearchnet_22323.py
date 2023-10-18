def create_patch(self, from_tag, to_tag):
        """Create a patch between tags"""
        return str(self._git.diff('{}..{}'.format(from_tag, to_tag), _tty_out=False))