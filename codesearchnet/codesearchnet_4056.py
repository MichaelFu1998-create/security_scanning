def root(self):
        """Root element for the page region.

        Page regions should define a root element either by passing this on
        instantiation or by defining a :py:attr:`_root_locator` attribute. To
        reduce the chances of hitting :py:class:`~selenium.common.exceptions.StaleElementReferenceException`
        or similar you should use :py:attr:`_root_locator`, as this is looked up every
        time the :py:attr:`root` property is accessed.
        """
        if self._root is None and self._root_locator is not None:
            return self.page.find_element(*self._root_locator)
        return self._root