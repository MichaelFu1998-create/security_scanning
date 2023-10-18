def finish_raw(self, body: bytes, status: int = 200, content_type: Optional[str] = None):
        """
        Set raw response
        :param body:
        :param status:
        :param content_type:
        :return:
        """
        self.ret_val = body
        self.response = web.Response(body=body, status=status, content_type=content_type)
        logger.debug('finish: raw body(%d bytes)' % len(body))
        self._finish_end()