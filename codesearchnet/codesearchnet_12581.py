async def _call_handle(self, func, *args):
        """ call and check result of handle_query/read/insert/update """
        await async_call(func, *args)

        if self.is_finished:
            raise FinishQuitException()