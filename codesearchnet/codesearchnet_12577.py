def finish(self, code, data=NotImplemented):
        """
        Set response as {'code': xxx, 'data': xxx}
        :param code:
        :param data:
        :return:
        """
        if data is NotImplemented:
            data = RETCODE.txt_cn.get(code, None)
        self.ret_val = {'code': code, 'data': data}  # for access in inhreads method
        self.response = web.json_response(self.ret_val, dumps=json_ex_dumps)
        logger.debug('finish: %s' % self.ret_val)
        self._finish_end()