def find_element(self, strategy, locator):
        """Finds an element on the page.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` or :py:attr:`~pypom.splinter_driver.ALLOWED_STRATEGIES`.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: An element.
        :rytpe: :py:class:`~selenium.webdriver.remote.webelement.WebElement` or :py:class:`~splinter.driver.webdriver.WebDriverElement`

        """
        return self.driver_adapter.find_element(strategy, locator, root=self.root)