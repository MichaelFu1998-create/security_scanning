def save_screenshot(self, filename, quietly = False):
        """Save the screenshot to local.

        Support:
            Android iOS Web(WebView)

        Args:
            filename(str): The path to save the image.
            quietly(bool): If True, omit the IOError when
                failed to save the image.

        Returns:
            WebElement Object.

        Raises:
            WebDriverException.
            IOError.
        """
        imgData = self.take_screenshot()
        try:
            with open(filename, "wb") as f:
                f.write(b64decode(imgData.encode('ascii')))
        except IOError as err:
            if not quietly:
                raise err