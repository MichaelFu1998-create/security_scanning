def add_element_extension_method(Klass):
    """Add element_by alias and extension' methods(if_exists/or_none)."""
    def add_element_method(Klass, using):
        locator = using.name.lower()
        find_element_name = "element_by_" + locator
        find_element_if_exists_name = "element_by_" + locator + "_if_exists"
        find_element_or_none_name = "element_by_" + locator + "_or_none"
        wait_for_element_name = "wait_for_element_by_" + locator

        find_elements_name = "elements_by_" + locator
        wait_for_elements_name = "wait_for_elements_by_" + locator

        def find_element(self, value):
            return self.element(using.value, value)

        find_element.__name__ = find_element_name
        find_element.__doc__ = (
            "Set parameter 'using' to '{0}'.\n".format(using.value) +
            "See more in \'element\' method."
        )

        def find_element_if_exists(self, value):
            return self.element_if_exists(using.value, value)

        find_element_if_exists.__name__ = find_element_if_exists_name
        find_element_if_exists.__doc__ = (
            "Set parameter 'using' to '{0}'.\n".format(using.value) +
            "See more in \'element_if_exists\' method."
        )

        def find_element_or_none(self, value):
            return self.element_or_none(using.value, value)

        find_element_or_none.__name__ = find_element_or_none_name
        find_element_or_none.__doc__ = (
            "Set parameter 'using' to '{0}'.\n".format(using.value) +
            "See more in \'element_or_none\' method."
        )

        def wait_for_element_by(self, *args, **kwargs):
            return self.wait_for_element(using.value, *args, **kwargs)

        wait_for_element_by.__name__ = wait_for_element_name
        wait_for_element_by.__doc__ = (
            "Set parameter 'using' to '{0}'.\n".format(using.value) +
            "See more in \'wait_for_element\' method."
        )

        def find_elements(self, value):
            return self.elements(using.value, value)

        find_elements.__name__ = find_elements_name
        find_elements.__doc__ = (
            "Set parameter 'using' to '{0}'.\n".format(using.value) +
            "See more in \'elements\' method."
        )

        def wait_for_elements_available(self, *args, **kwargs):
            return self.wait_for_elements(using.value, *args, **kwargs)

        wait_for_elements_available.__name__ = wait_for_elements_name
        wait_for_elements_available.__doc__ = (
            "Set parameter 'using' to '{0}'.\n".format(using.value) +
            "See more in \'wait_for_elements\' method."
        )

        setattr(Klass, find_element_name, find_element)
        setattr(Klass, find_element_if_exists_name, find_element_if_exists)
        setattr(Klass, find_element_or_none_name, find_element_or_none)
        setattr(Klass, wait_for_element_name, wait_for_element_by)
        setattr(Klass, find_elements_name, find_elements)
        setattr(Klass, wait_for_elements_name, wait_for_elements_available)

    for locator in iter(Locator):
        add_element_method(Klass, locator)