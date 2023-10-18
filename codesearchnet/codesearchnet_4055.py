def register():
    """ Register the Selenium specific driver implementation.

        This register call is performed by the init module if
        selenium is available.
    """
    registerDriver(
        ISelenium,
        Selenium,
        class_implements=[
            Firefox,
            Chrome,
            Ie,
            Edge,
            Opera,
            Safari,
            BlackBerry,
            PhantomJS,
            Android,
            Remote,
            EventFiringWebDriver,
        ],
    )