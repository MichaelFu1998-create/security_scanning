async def login(self, user=DEFAULT_USER, password=DEFAULT_PASSWORD,
                    account=DEFAULT_ACCOUNT):
        """
        :py:func:`asyncio.coroutine`

        Server authentication.

        :param user: username
        :type user: :py:class:`str`

        :param password: password
        :type password: :py:class:`str`

        :param account: account (almost always blank)
        :type account: :py:class:`str`

        :raises aioftp.StatusCodeError: if unknown code received
        """
        code, info = await self.command("USER " + user, ("230", "33x"))
        while code.matches("33x"):
            if code == "331":
                cmd = "PASS " + password
            elif code == "332":
                cmd = "ACCT " + account
            else:
                raise errors.StatusCodeError("33x", code, info)
            code, info = await self.command(cmd, ("230", "33x"))