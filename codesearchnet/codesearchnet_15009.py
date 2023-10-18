def tag(self, label, message=None):
        """Tag the current workdir state."""
        notify.warning('Unsupported SCM: Make sure you apply the "{}" tag after commit!{}'.format(
            label, ' [message={}]'.format(message) if message else '',
        ))