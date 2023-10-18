def wait_for(
        self, timeout=10000, interval=1000,
        asserter=lambda x: x):
        """Wait for driver till satisfy the given condition

        Support:
            Android iOS Web(WebView)

        Args:
            timeout(int): How long we should be retrying stuff.
            interval(int): How long between retries.
            asserter(callable): The asserter func to determine the result.

        Returns:
            Return the driver.

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
        def _wait_for(driver):
            asserter(driver)
            return driver

        return _wait_for(self)