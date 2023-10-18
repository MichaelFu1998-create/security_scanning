def wait_for_elements(
        self, using, value, timeout=10000,
        interval=1000, asserter=is_displayed):
        """Wait for elements till satisfy the given condition

        Support:
            Android iOS Web(WebView)

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.
            timeout(int): How long we should be retrying stuff.
            interval(int): How long between retries.
            asserter(callable): The asserter func to determine the result.

        Returns:
            Return the list of Element if any of them satisfy the condition.

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
        def _wait_for_elements(ctx, using, value):
            els = ctx.elements(using, value)
            if not len(els):
                raise WebDriverException('no such element')
            else:
                el = els[0]
                asserter(el)
                return els

        return _wait_for_elements(self, using, value)