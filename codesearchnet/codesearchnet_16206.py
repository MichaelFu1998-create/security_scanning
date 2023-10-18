def wait_for_element(
        self, using, value, timeout=10000,
        interval=1000, asserter=is_displayed):
        """Wait for element till satisfy the given condition

        Support:
            Android iOS Web(WebView)

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.
            timeout(int): How long we should be retrying stuff.
            interval(int): How long between retries.
            asserter(callable): The asserter func to determine the result.

        Returns:
            Return the Element.

        Raises:
            WebDriverException.
        """
        if not callable(asserter):
            raise TypeError('Asserter must be callable.')
        @retry(
            retry_on_exception=lambda ex: isinstance(ex, WebDriverException),
            stop_max_delay=timeout,
            wait_fixed=interval
        )
        def _wait_for_element(ctx, using, value):
            el = ctx.element(using, value)
            asserter(el)
            return el

        return _wait_for_element(self, using, value)