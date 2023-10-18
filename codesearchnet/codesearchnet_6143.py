def _fail(self, value, context_info=None, src_exception=None, err_condition=None):
        """Wrapper to raise (and log) DAVError."""
        e = DAVError(value, context_info, src_exception, err_condition)
        if self.verbose >= 4:
            _logger.warning(
                "Raising DAVError {}".format(
                    safe_re_encode(e.get_user_info(), sys.stdout.encoding)
                )
            )
        raise e